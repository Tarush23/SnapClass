import streamlit as st
from src.components.headers import header_dashboard
from src.ui.base_layout import style_background_dashboard,style_base_layout
from src.components.footer import footer_dashboard

def teacher_screen():
    style_background_dashboard()
    style_base_layout() 

    if "teacher_login_type" not in st.session_state or st.session_state["teacher_login_type"]=="login":
        teacher_screen_login()
    elif st.session_state["teacher_login_type"]=="register":
        teacher_screen_register()

    footer_dashboard()


def teacher_screen_login():
    c1,c2 = st.columns(2, vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("go back to home",type='secondary',key="loginbackbutton",shortcut="control+backspace"):
            #important feature
            st.session_state["login_type"]=None
            st.rerun()

    
    st.header("Login using password",text_alignment="center")

    teacher_username = st.text_input("Enter username",placeholder="jatingupta")
    teacher_pass = st.text_input("Enter password",type="password",placeholder="enter password")

    st.divider()

    btnc1,btnc2 = st.columns(2)

    with btnc1:
        st.button("Login",icon=":material/passkey:",shortcut='control+enter',width='stretch')

    with btnc2:
        if st.button("Register",type="primary",icon=":material/passkey:",shortcut="control+enter",width="stretch"):
            st.session_state["teacher_login_type"]="register"


def teacher_screen_register():
    c1,c2 = st.columns(2, vertical_alignment='center',gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("go back to home",type='secondary',key="loginbackbutton",shortcut="control+backspace"):
            st.session_state["login_type"]=None
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
        st.button("Register Now",type="primary",icon=":material/passkey:",shortcut="control+enter",width="stretch")
            



