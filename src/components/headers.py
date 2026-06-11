import streamlit as st


def header_home():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(
        f"""
            <div style="text-align:center;">
                <img src="{logo_url}" style="height:100px;">
                <h1>
                    Snap<br/>Class
                </h1>
            </div>
        """,
        unsafe_allow_html=True
    )


def header_dashboard():
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        f"""
            <div style="display:flex;align-items:center;gap:xxlarge;">
                <img src="{logo_url}" style="height:100px;">
                <h2 style="text-align:left; color:#5865F2">
                    Snap<br/>Class
                </h2>
            </div>
        """,
        unsafe_allow_html=True
    )

