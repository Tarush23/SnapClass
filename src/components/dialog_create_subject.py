import streamlit as st
from src.database.db import create_subject

@st.dialog("create new subject")
def create_subject_dialog(teacher_id):
    st.write("eneter details of the new subject")
    sub_code = st.text_input("subject code",placeholder="CS101")
    sub_name = st.text_input("Subject name",placeholder="Introduction to computer science")
    sub_section = st.text_input("Section",placeholder="A")

    if st.button("Create subject now",type="primary",width="stretch"):
        if sub_code and sub_name and sub_section:
            try:
                create_subject(sub_code,sub_name,sub_section,teacher_id)
                st.toast("subject created successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

        else:
            st.warning("Pls fill all the fields")