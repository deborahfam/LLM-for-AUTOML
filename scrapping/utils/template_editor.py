import streamlit as st
import os
from utils.templates import save_template


def template_editor():
    st.header("Template Editor")
    new_extract_template = st.text_area(
        "Extract Template", st.session_state["extract_template"], height=500
    )

    template_name = st.text_input("Template Name", "main.json")

    if st.button("Save Template"):
        template = {
            "extract_template": new_extract_template,
        }
        save_template(template, os.path.join("templates", template_name))
        st.success(f"Template saved as {template_name}")

    st.session_state["extract_template"] = new_extract_template
