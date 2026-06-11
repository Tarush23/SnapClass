import streamlit as st
from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

def main():
    if "login_type" not in st.session_state:
        #print(st.session_state)
        st.session_state["login_type"]=None

    match st.session_state["login_type"]:
        case "teacher":
            teacher_screen()
        case "student":
            student_screen()
        case None:
            home_screen()
            print("rerun")
            
main()
# # stream lit basics

# def main():
#     st.header("basics of streamlit")

#     name = st.text_input("enter your name")

#     col1,col2=st.columns(2,gap="small")
#     with col1:
#         if st.button("click me",type="primary",width="stretch"):
#             print(name)

#     with col2:
#         st.button("click ",type="primary")


#     st.markdown(r"""
#     <div>
#         <h3>image through html</h3>
#     </div>
# """, unsafe_allow_html=True)


# main()
