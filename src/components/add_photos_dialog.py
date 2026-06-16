import streamlit as st
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write(
        "Add classroom photos to scan for attendance"
    )

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    if "cam_processed" not in st.session_state:
        st.session_state.cam_processed = False

    if "upload_processed" not in st.session_state:
        st.session_state.upload_processed = False

    t1, t2 = st.columns(2)

    with t1:

        if st.button(
            "Camera",
            type=(
                "primary"
                if st.session_state.photo_tab == "camera"
                else "tertiary"
            ),
            width="stretch"
        ):
            st.session_state.photo_tab = "camera"

    with t2:

        if st.button(
            "Upload photos",
            type=(
                "primary"
                if st.session_state.photo_tab == "upload"
                else "tertiary"
            ),
            width="stretch"
        ):
            st.session_state.photo_tab = "upload"

    # CAMERA
    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input(
            "Take Snapshot",
            key="dialog_cam"
        )

        if (
            cam_photo
            and
            not st.session_state.cam_processed
        ):

            st.session_state.attendance_images.append(
                Image.open(cam_photo)
            )

            st.session_state.cam_processed = True

            st.toast(
                "Photo Captured"
            )

        elif not cam_photo:
            st.session_state.cam_processed = False

    # UPLOAD
    if st.session_state.photo_tab == "upload":

        uploaded_files = st.file_uploader(
            "Choose image files",
            type=[
                "jpg",
                "png",
                "jpeg"
            ],
            accept_multiple_files=True,
            key="dialog_upload"
        )

        if (
            uploaded_files
            and
            not st.session_state.upload_processed
        ):

            st.session_state.attendance_images.extend(
                [
                    Image.open(f)
                    for f in uploaded_files
                ]
            )

            st.session_state.upload_processed = True

            st.toast(
                "Photos Uploaded Successfully"
            )

        elif not uploaded_files:
            st.session_state.upload_processed = False

    st.divider()

    if st.button(
        "Done",
        type="primary",
        width="stretch"
    ):

        st.session_state.cam_processed = False
        st.session_state.upload_processed = False

        st.rerun()