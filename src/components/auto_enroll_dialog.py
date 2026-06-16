import streamlit as st
from src.database.db import check_code,enroll_student,already_enrolled
from src.database.config import supabase
import time 

@st.dialog("Quick enrollment")
def auto_enroll_subject(join_code):
    student_id = st.session_state["student_data"]["student_id"]

    res = supabase.table("subjects").select("subject_id,name").eq("subject_code",join_code).execute()

    if not res.data:
        st.error("subject code not found")
        if st.button("close"):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]

    subject_id = subject["subject_id"]

    res = already_enrolled(subject_id,student_id)


    if res:
        st.info("you are already enrolled")
        if st.button("close"):
            st.query_params.clear()
            st.rerun()
        return
    
    st.markdown(f'would you like to enroll in **(subject["name"])**?')

    col1,col2 = st.columns(2)

    with col1:
        if st.button("no thanks"):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button("yes enroll now:",type="primary",width='stretch'):
            enroll_student(subject_id,student_id)
            st.success("joined successfully")
            st.query_params.clear()
            time.sleep(2)
            st.rerun()



