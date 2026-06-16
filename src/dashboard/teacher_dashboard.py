import streamlit as st
from src.components.headers import header_dashboard
from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)
from src.components.footer import footer_dashboard

from src.components.dialog_create_subject import create_subject_dialog
from src.database.db import get_teacher_subjects,get_subject_attendance
from src.components.subject_card import subject_card
from src.components.share_subject_dialog import share_subject_dialog
from src.components.add_photos_dialog import add_photos_dialog
import numpy as np
from src.pipelines.face_recoginition import predict_attendance
from src.database.config import supabase
from datetime import datetime
import pandas as pd

from src.components.dialog_attendance_results import attendance_result_dialog
from src.components.voice_attendance_dialog import voice_attendance_dialog


def teacher_dashboard():
    style_background_dashboard()
    style_base_layout()

    teacher_data = st.session_state.get("teacher_data")
    if not teacher_data:
        st.warning("Teacher not logged in")
        return

    st.header(
        f"welcome back, {teacher_data['name']}"
    )

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "logout",
            type="secondary",
            key="logout_button",
            shortcut="control+backspace"
        ):
            st.session_state["teacher_login_type"] = "login"

            del st.session_state["teacher_data"]

            st.session_state.is_logged_in = False

            st.rerun()

    st.space()
    st.space()

    tab1,tab2,tab3 = st.columns(3)

    
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab=None

    with tab1:
        type1="primary" if st.session_state.current_teacher_tab =="take_attendance" else "tertiary"
        if st.button("take attendance",type = type1,width="stretch",icon=":material/ar_on_you:"):
            st.session_state.current_teacher_tab="take_attendance"
            st.rerun()

    with tab2:
        type2="primary" if st.session_state.current_teacher_tab == "manage_subjects" else "tertiary"
        if st.button("manage subjects",type = type2,width="stretch",icon=":material/book_ribbon:"):
            st.session_state.current_teacher_tab="manage_subjects"
            st.rerun()


    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab=="attendance_records" else "tertiary"
        if st.button("attendance records",width="stretch",type = type3,icon=":material/cards_stack:"):
            st.session_state.current_teacher_tab="attendance_records"
            st.rerun()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendance()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()


    footer_dashboard()


def teacher_tab_take_attendance():
    teacher_data = st.session_state["teacher_data"]
    teacher_id = teacher_data["teacher_id"]

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("you havent created any subjects yet! pls create one to begin")
        return
    
    subjects_options = {}

    for subject in subjects:
        option_label = (
            f"{subject['name']}-"f"{subject['subject_code']}"
        )

        subjects_options[option_label]=subject["subject_id"]

    col1,col2 = st.columns([3,1])  # this means that space by col1 and col2 is in 3:1 ratio

    with col1:
        selected_subject_label = st.selectbox("select subject",options = list(subjects_options.keys()))

    with col2:
        if st.button("add photos",type="primary"):
            add_photos_dialog()

    selected_subject_id = subjects_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header("added photos")
        gallery_cols = st.columns(4)

        for idx,img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx%4]:
                st.image(img,width="stretch",caption=f"Photo {idx+1}")

    # 3 options : retake,analyse,use voice attendance

    c1,c2,c3 = st.columns(3)

    with c1:
        if st.button("clear all photos",width="stretch",type="primary"):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button("Run face analysis",width="stretch",type="secondary"):
            with st.spinner("Deep scanning classroom photos"):
                all_detected_id = {}

                for idx,img in enumerate(st.session_state.attendance_images):
                    img_np=np.array(img)

                    detected,_,_ = predict_attendance(img_np)

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_id[student_id]=f"photo {idx+1}"

                enrolled_res = supabase.table("subject_students").select("*,students(*)").eq("subject_id",selected_subject_id).execute()

                enrolled_students = enrolled_res.data

                if not enrolled_students :
                    st.warning("no students enrolled in this course")
                else:

                    results,attendance_to_log = [],[]

                    current_timestamp = datetime.now().strftime("%Y=%m-%dT%H:%M:%S")

                    for node in enrolled_students:
                        student = node['students']

                        sources=all_detected_id.get(int(student["student_id"]),[])

                        is_present = len(sources)>0

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

                    attendance_result_dialog(pd.DataFrame(results),attendance_to_log)

    with c3:
        if st.button("Use voice attendance",type="primary",width="stretch"):
            voice_attendance_dialog(selected_subject_id)

        
def teacher_tab_manage_subjects():
    st.space()
    teacher_data = st.session_state["teacher_data"]
    teacher_id = teacher_data["teacher_id"]
    col1,col2 = st.columns(2)
    with col1:
        st.header("manage subjects",width="stretch")
    with col2:
        if st.button("create new subject",width="stretch"):
            create_subject_dialog(teacher_id)
    

    # list all the subjects
    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("","students",sub["total_students"]),
                ("","classes",sub["total_classes"])
            ]
            def share_btn():
                if st.button(f"share code:{sub["name"]}",key=f"share_{sub['subject_code']}",icon=":material/share:"):
                    share_subject_dialog(sub["name"],sub["subject_code"])

                st.space() 

            subject_card(
                name=sub["name"],
                code = sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn
            )
    else:
        st.info("no subjects found. create one above")

def teacher_tab_attendance_records():
    teacher_data = st.session_state["teacher_data"]
    teacher_id = teacher_data["teacher_id"]
    st.header("Attendance Records")
    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("you havent created any subjects yet! pls create one to begin")
        return
    
    subjects_options = {}

    for subject in subjects:
        option_label = (
            f"{subject['name']}-"f"{subject['subject_code']}"
        )

        subjects_options[option_label]=subject["subject_id"]

    selected_subject_label = st.selectbox("select subject for which attendance is to be viewed",options = list(subjects_options.keys()))

    selected_subject_id = subjects_options[selected_subject_label]

    response = get_subject_attendance(selected_subject_id)

    if not response:
        st.write("No attendance records found")
    else:
        #st.write(response)

        data = []

        for r in response:
            dt = datetime.fromisoformat(r["timestamp"])
            date = dt.date()
            time = dt.time()
            data.append({
                "student name" : r["students"]["name"],
                "Date":dt.strftime("%d %b %Y"),
                "Time":dt.strftime("%I:%M %p")
            })

        df = pd.DataFrame(data)

        st.dataframe(df,hide_index=True,width="stretch")