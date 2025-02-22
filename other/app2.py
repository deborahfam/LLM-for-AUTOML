import streamlit as st
import os
from handler import LLMHandler
from fireworks import Firework
from other.embeddings import LMStudioEmbedding

st.title("Simple Crawler")
model_embedding = LMStudioEmbedding()
llm_handler = LLMHandler(model_embedding)


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "augmented_messages" not in st.session_state:
        st.session_state.augmented_messages = []
    if "llm" not in st.session_state:
        st.session_state["llm"] = "accounts/fireworks/models/mixtral-8x7b-instruct"

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def submit_to_llm():
    return llm_handler.client.chat.completions.create(
        model=st.session_state["llm"],
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.augmented_messages if m["role"] == "user"
        ][-4:],
        stream=True,
        temperature=0.7,
    )

def handle_user_input():
    prompt = st.chat_input("Ask questions about the article")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            #refined_prompt =llm_handler.get_response(prompt)
            st.session_state.augmented_messages.append({"role": "user", "content": prompt})
            stream = submit_to_llm()
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.augmented_messages.append({"role": "assistant", "content": response})

def ChatBot():
    st.title("Ask questions about the PDF")
    display_chat_history()
    handle_user_input()

def main():
    initialize_session_state()
    st.set_page_config(page_title="Chatbot", page_icon="💬")
    ChatBot()

if __name__ == "__main__":
    main()