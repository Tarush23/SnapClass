import streamlit as st
from src.pipelines.voice_recoginition import process_bulk_audio
from src.database.config import supabase
import time
from datetime import datetime
from src.components.dialog_attendance_results import show_attendance_results
import pandas as pd


@st.dialog("Take voice attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write("Record audio of students saying I am present. Then AI will recognize the students")

    audio_data = None

    try:
        audio_data = st.audio_input("Record audio")
    except Exception:
        st.error("audio data failed")

    if audio_data:
        if st.button("analyze audio"):
            with st.spinner("Analyzing audio"):
                #first get all the students enrolled in that subject
                response = supabase.table("subject_students").select("*,students(*)").eq("subject_id",selected_subject_id).execute()

                existing_students = response.data

                if not existing_students:
                    st.warning("no students enrolled in the course")
                    st.sleep(2)
                    st.rerun()
                else:
                    candidates_dict={}

                    for s in existing_students:
                        if(s["students"].get("voice_embedding")):
                            candidates_dict[s["students"]["student_id"]] = s["students"]["voice_embedding"]

                    if not candidates_dict:
                        st.error("no enrolled students have voice profiles")
                        time.sleep(2)
                        st.rerun()

                    detected_scores = process_bulk_audio(audio_data.read(),candidates_dict)

                    results,attendance_to_log = [],[]

                    current_timestamp = datetime.now().strftime("%Y=%m-%dT%H:%M:%S")

                    for node in existing_students:
                        student = node['students']

                        score=detected_scores.get(int(student["student_id"]),0.0)

                        is_present = bool(score>0)

                        results.append({
                            "Name":student["name"],
                            "ID":student["student_id"],
                            "Status":"Present" if is_present else "Absent"
                        })

                        attendance_to_log.append({
                            "student_id":student["student_id"],
                            "subject_id":selected_subject_id,
                            "timestamp":current_timestamp,
                            "is_present":bool(is_present)
                        })

                    st.session_state.voice_attendance_results = pd.DataFrame(results),attendance_to_log

    if st.session_state.get("voice_attendance_results"):
        st.divider()
        df_results,logs = st.session_state.voice_attendance_results
        show_attendance_results(df_results,logs)
        st.session_state.get("voice_attendance_results")
