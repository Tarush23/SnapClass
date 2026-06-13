import streamlit as st
from src.components.headers import header_dashboard
from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)
from src.components.footer import footer_dashboard

from src.components.dialog_create_subject import create_subject_dialog
from src.database.db import get_teacher_subjects
from src.components.subject_card import subject_card
from src.components.share_subject_dialog import share_subject_dialog


def teacher_dashboard():
    style_background_dashboard()
    style_base_layout()

    teacher_data = st.session_state.get("teacher_data")
    print(teacher_data)

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
    st.header("Take AI attendance")


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
    st.header("manage attendance")