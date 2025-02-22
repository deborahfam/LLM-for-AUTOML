# app.py
import streamlit as st
from dotenv import load_dotenv
from services.api_service import Client_Handler
from services.message_history import Message_Handler
from model_config import MODEL_CONFIGURATIONS
# from app_state import initialize_state  

# Configuración inicial
st.set_page_config(page_title="Chat con LM Studio", page_icon="🤖")
st.title("🧠 Chatbot")

load_dotenv() 
# initialize_state()  
history = Message_Handler(MODEL_CONFIGURATIONS["DeepSeek R1"])
client_handler = Client_Handler()
# history.display_chat_history() 

if prompt := st.chat_input("Hazme una pregunta..."):
    history.add_message("user",prompt)
    history.display_chat_history()
    
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            response = client_handler.submit_to_llm()  # Removed await since it's not in an async function
            
        st.write(response)
        history.add_message("assistant", response)
