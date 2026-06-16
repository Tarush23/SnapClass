import streamlit as st

from src.components.headers import header_dashboard
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.footer import footer_dashboard

from PIL import Image
import numpy as np

from src.pipelines.face_recoginition import predict_attendance,get_face_embeddings,train_classifier
from src.pipelines.voice_recoginition import get_voice_embedding

from src.database.db import get_all_students,create_student
import time

from src.dashboard.student_dashboard import student_dashboard


def student_screen():
    show_registration=False
    style_background_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
    
    c1,c2 = st.columns(2,vertical_alignment="center",gap="xxlarge")

    with c1:
        header_dashboard()
    with c2:
        if st.button("go back home",type="secondary",key="loginbackbutton",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()

    st.header("Login using FaceID",text_alignment="center")


    photo_source = st.camera_input("Position your face in the center")

    if photo_source :
        img = np.array(Image.open(photo_source))

        with st.spinner("AI is scanning....."):
            detected , all_ids,num_faces = predict_attendance(img)

            if num_faces == 0:
                st.warning("face not found")

            elif num_faces > 1:
                st.warning("multiple faces found")
            
            else:
                if detected :
                    student_id = list(detected.keys())[0]

                    all_students = get_all_students()

                    student_found = None

                    for student in all_students:
                        if student["student_id"]==student_id :
                            student_found = student
                            break
                    
                    if student_found:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state["student_data"] = student_found

                        st.toast(f"welcome back {student_found["name"]}")
                        time.sleep(2)
                        st.rerun()

                else:
                    st.info("face not recognized! you might be a new student")
                    show_registration=True
                
        if show_registration:
            with st.container(border=True):
                st.header("register your profile")
                new_name = st.text_input("Enter your name", placeholder='E.g. Hamza Rizvi')

                st.subheader('Optional : Voice Enrollment')
                st.info("Enroll your for voice only attendance")

                audio_data = None

                try:
                    audio_data = st.audio_input("record a short phrase like i am present,My name is abhishek")
                except Exception:
                    st.error("audio data failed")

                if st.button("Create account",type="primary"):
                    if new_name : 
                        with st.spinner("creating profile...."):
                            img = np.array(Image.open(photo_source))
                            encodings = get_face_embeddings(img)

                            if encodings:
                                face_emb = encodings[0].tolist()

                                voice_emb = None
                                if audio_data :
                                    voice_emb = get_voice_embedding(audio_data.read())

                                response_data = create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)

                                if response_data :
                                    train_classifier()
                                    st.session_state.is_logged_in = True
                                    st.session_state.user_role = 'student'
                                    st.session_state["student_data"] = response_data[0]
                                    st.toast(f'Profile Created! Hi {new_name}!')
                                    time.sleep(1)
                                    st.rerun()
                            else:
                                st.error("coludnt capture your facial features for registration")
                    else:
                        st.warning("pls enter your name")

    footer_dashboard()


