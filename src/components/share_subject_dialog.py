import streamlit as st
from src.ui.base_layout import style_base_layout

import segno
import io

@st.dialog("Share Class Link")
def share_subject_dialog(subject_name,subject_code):
    app_domain="http://localhost:8501/"
    join_url=f"{app_domain}?join_code={subject_code}"

    st.header("Scan to join")

    qr = segno.make("Scan to join")

    out = io.BytesIO()

    qr.save(out,kind="png",scale=10,border=1)

    col1,col2=st.columns(2)

    with col1:
        st.markdown("copy link")
        st.code(join_url,language="text")
        st.code(subject_code,language="text")
        st.info("copy think link to share on whatsapp")

    with col2:
        st.markdown("scan to join")
        st.image(out.getvalue(),caption="OR code for class joining")