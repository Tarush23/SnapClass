import streamlit as st
from src.ui.base_layout import (
    style_background_dashboard,
    style_base_layout
)

from src.components.headers import (
    header_dashboard
)

from src.components.footer import (
    footer_dashboard
)

from src.components.dialog_subject_enroll import (
    enroll_subject_dialog
)

from src.database.db import (
    get_student_subjects,
    get_student_attendance
)


def student_dashboard():

    style_background_dashboard()
    style_base_layout()

    student_data = (
        st.session_state["student_data"]
    )

    student_id = (
        student_data["student_id"]
    )

    student_name = (
        student_data["name"]
    )

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge"
    )

    with c1:
        header_dashboard()

    with c2:

        st.header(
            f"welcome back {student_data['name']}"
        )

        if st.button(
            "logout",
            type="secondary",
            key="logout_button",
            shortcut="control+backspace"
        ):

            del st.session_state[
                "student_data"
            ]

            st.session_state[
                "is_logged_in"
            ] = False

            st.rerun()

    st.space()
    st.space()

    c1, c2 = st.columns(2)

    with c1:
        st.header(
            "your enrolled subjects"
        )

    with c2:

        if st.button(
            "Enroll in subject",
            type="primary",
            width="stretch"
        ):

            enroll_subject_dialog(
                student_id,
                student_name
            )

    with st.spinner(
        "loading your subjects"
    ):

        subjects = (
            get_student_subjects(
                student_id
            )
        )

        logs = (
            get_student_attendance(
                student_id
            )
        )

        # -------------------
        # Build attendance stats
        # -------------------

        stats_map = {}

        for log in logs:

            sid = log["subject_id"]

            if sid not in stats_map:

                stats_map[
                    sid
                ] = {

                    "total": 0,

                    "attended": 0
                }

            stats_map[
                sid
            ][
                "total"
            ] += 1

            if log.get(
                "is_present"
            ):

                stats_map[
                    sid
                ][
                    "attended"
                ] += 1

        # -------------------
        # Merge subjects
        # -------------------

        final_attendance_list = {}

        for subject in subjects:

            subject_info = (
                subject
                .get(
                    "subjects",
                    {}
                )
            )

            sub_name = (
                subject_info
                .get(
                    "name",
                    "Unknown"
                )
            )

            sub_id = (
                subject[
                    "subject_id"
                ]
            )

            data = (
                stats_map
                .get(
                    sub_id,
                    {
                        "total": 0,
                        "attended": 0
                    }
                )
            )

            final_attendance_list[
                sub_name
            ] = {

                "total":
                data["total"],

                "attended":
                data["attended"]
            }
        
        # -------------------
        # Create table rows
        # -------------------

        rows = []

        # st.write(subjects)
        # st.write(stats_map)
        # st.write(final_attendance_list)

        for subject, data in (
            final_attendance_list.items()
        ):

            rows.append({

                "Subject":
                subject,

                "Total Classes":
                data[
                    "total"
                ],

                "Attended":
                data[
                    "attended"
                ],

                "Attendance %":

                round(

                    (
                        data[
                            "attended"
                        ]

                        /

                        data[
                            "total"
                        ]

                        * 100

                    )

                    if data[
                        "total"
                    ]

                    else 0,

                    1
                )
            })

        # -------------------
        # Display table
        # -------------------

        st.dataframe(
            rows
        )

    footer_dashboard()

