import json
import streamlit as st
import re


def display_response_with_figures(text, images_captions):
    pattern = re.compile(r"#Figure \d+(.*?)(?=\n\n|$)", re.DOTALL)
    last_pos = 0
    fig_count = 0

    for match in pattern.finditer(text):
        st.markdown(text[last_pos : match.start()])
        if fig_count < len(images_captions):
            image, caption = images_captions[fig_count]
            if image:  # Verifica si la imagen realmente existe
                st.image(image, caption=caption, width=400)
            fig_count += 1
        last_pos = match.end()

    if last_pos < len(text):
        st.markdown(text[last_pos:])


def valid_json(json_response):
    # TODO: Use pydantic models if validation of different structured json is needed
    try:
        data = json.loads(json_response.strip())
    except json.JSONDecodeError:
        return False, "El JSON no es válido."
    if "questions" not in data:
        return False, "El JSON no contiene el objeto 'questions'."
    questions = data["questions"]
    if not isinstance(questions, list) or not all(
        isinstance(q, str) for q in questions
    ):
        return False, "El objeto 'questions' no contiene preguntas de tipo string."
    return True
