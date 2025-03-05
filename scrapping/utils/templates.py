import streamlit as st
import json

# TODO: Use a template framework like jinja to create more diverse and powerful prompt templates


def save_template(template, file_name):
    with open(file_name, "w") as file:
        # FIXME: Avoid using json without sense. It's just a text, write and read text.
        json.dump(template, file)


def load_template(file_name):
    with open(file_name, "r") as file:
        template = json.load(file)
    # FIXME: Change use of streamlit for something different. Avoid using session state
    st.session_state["extract_template"] = template.get("extract_template", "")
