import streamlit as st
from src.components.headers import header_dashboard
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.footer import footer_dashboard

from src.database.db import create_teacher,check_teacher_exists,teacher_login

import time

def teacher_screen():
    style_background_dashboard()
    style_base_layout() 

    
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state["teacher_login_type"]=="login":
        teacher_screen_login()
    elif st.session_state["teacher_login_type"]=="register":
        teacher_screen_register()

    footer_dashboard()


def teacher_dashboard():
    teacher_data = st.session_state["teacher_data"]
    st.header(f"welcome back {teacher_data["name"]}")

def teacher_screen_login():
    c1,c2 = st.columns(2, vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("go back to home",type='secondary',key="loginbackbutton",shortcut="control+backspace"):
            #important feature
            st.session_state["teacher_login_type"]=None
            st.rerun()

    
    st.header("Login using password",text_alignment="center")

    teacher_username = st.text_input("Enter username",placeholder="jatingupta")
    teacher_pass = st.text_input("Enter password",type="password",placeholder="enter password")

    st.divider()

    btnc1,btnc2 = st.columns(2)

    with btnc1:
        if st.button("Login",icon=":material/passkey:",shortcut='control+enter',width='stretch'):
            success,message = login_teacher(teacher_username,teacher_pass)

            if success:
                st.success(message)
                st.rerun()
            elif not success:
                st.error(message)

    with btnc2:
        if st.button("Register",type="primary",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            st.session_state["teacher_login_type"]="register"


def teacher_screen_register():
    c1,c2 = st.columns(2, vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("go back to home",type='secondary',key="loginbackbutton",shortcut="control+backspace"):
            st.session_state["teacher_login_type"]=None
            st.rerun()
    
    st.header("Register yourself as Teacher",text_alignment="center")

    teacher_name = st.text_input("Enter name",placeholder="Jatin Gupta")
    teacher_username = st.text_input("Enter username",placeholder="jatingupta")
    teacher_pass = st.text_input("Enter password",type="password",placeholder="enter password")
    teacher_pass_confirm = st.text_input("Confirm password",placeholder="Re-enter the password",type="password")

    st.divider()

    btnc1,btnc2 = st.columns(2)

    with btnc1:
        if st.button("Login",icon=":material/passkey:",shortcut='control+enter',width='stretch'):
            st.session_state["teacher_login_type"]="login"

    with btnc2:
        if st.button("Register Now",type="primary",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            success,message = register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm)

            if success:
                st.success(message)
                time.sleep(2)
                st.session_state["teacher_login_type"]="login"
                st.rerun()
            else:
                st.error(message)
                print(message)



def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):

    # validation part
    if not teacher_username or not teacher_name or not teacher_pass:
        return False ,"all fields are required"
    
    if check_teacher_exists(teacher_username):
        return False,"Username already exists"
    
    if teacher_pass != teacher_pass_confirm:
        return False,"Password doesnt match"
    

    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"Successfully created login now"
    except Exception as e:
        return False,e      


def login_teacher(teacher_username,teacher_pass):
    if not teacher_username or not teacher_pass:
        return False,"all fields are required"

    if not check_teacher_exists(teacher_username):
        return False,"teacher not registered"
    
    try:
        teacher = teacher_login(teacher_username,teacher_pass)

        if teacher:
            st.session_state.user_role="teacher"
            st.session_state["teacher_data"] = teacher
            st.session_state.is_logged_in = True
        return True,"successfully logged in"
    except Exception as e:
        return False,e



