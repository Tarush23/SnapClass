import streamlit as st
from src.database.db import check_code,enroll_student,already_enrolled
from src.database.config import supabase
import time 

@st.dialog("Enroll in subject")
def enroll_subject_dialog(student_id,student_name):
    st.info("enter the subject code provided by your teacher to enroll")
    join_code = st.text_input("Subject code",placeholder="10101")

    if st.button("Enroll now",type="primary",width="stretch"):
        if join_code : 
            response = check_code(join_code)
            if not response:
                st.warning("pls enter a valid subject code")
            else:
                response = supabase.table("subjects").select("subject_id").eq("subject_code",join_code).execute()

                subject_id = response.data[0]["subject_id"]
                if not already_enrolled(subject_id,student_id):
                    try:
                        enroll_student(subject_id,student_id)
                        st.success("enrolled successfully")
                        time.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.warning(e)

                else:
                    st.warning("already enrolled in the subject")
        else:
            st.warning("pls enter a subject code to join")