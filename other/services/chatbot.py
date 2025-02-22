import streamlit as st

class ChatbotService:
    def __init__(self, model_embedding, llm_handler) -> None:
        self.embedding = model_embedding
        self.handler = llm_handler

    def submit_to_llm(self, temperature, top_p, messages):
        return self.handler.client.chat.completions.create(
            model=st.session_state["llm"],
            messages=messages,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        )

    def submit_to_chatGPT(self, messages):
        return self.handler.chatGPTclient.chat.completions.create(
            model="gpt-4o", messages=messages, stream=True
        )
