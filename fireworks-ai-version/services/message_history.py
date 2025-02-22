import datetime, os
import streamlit as st

class Message_Handler:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name["model_name"]
        if "messages" not in st.session_state:
            st.session_state.messages = []

    def add_message(self, role: str, content: str):
        st.session_state.messages.append({"role": role, "content": content})
        # self.save_log()

    def get_last_k_messages(self, k: int):
        return st.session_state.messages[-k:]   
     
    def get_context(self):
        user_messages = [msg for msg in st.session_state.messages if msg["role"] == "user"]
        return [{"role": "user", "content": user_messages[-1]["content"]}] if user_messages else []

    def display_chat_history(self, k: int = 5):
        messages_to_display = self.get_last_k_messages(k)
        for message in messages_to_display:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    def clear_history(self):
        st.session_state.messages = []

    def count_tokens(self, text: str) -> int:
        return len(text.split())

    def is_token_count_below(self, text: str, limit: int) -> bool:
        token_count = self.count_tokens(text)
        return token_count < limit
    
    def get_all_messages(self):
       return st.session_state.messages
    
    def get_last_n_user_messages(self, n: int):
       user_messages = [msg for msg in st.session_state.messages if msg["role"] == "user"]
       return user_messages[-n:] if len(user_messages) >= n else user_messages
    
    def get_last_n_assistant_messages(self, n: int):
       assistant_messages = [msg for msg in st.session_state.messages if msg["role"] == "assistant"]
       return assistant_messages[-n:] if len(assistant_messages) >= n else assistant_messages
    
    def remove_message_by_index(self, index: int):
       if 0 <= index < len(st.session_state.messages):
           del st.session_state.messages[index]

    def update_message(self, index: int, new_content: str):
       if 0 <= index < len(st.session_state.messages):
           st.session_state.messages[index]["content"] = new_content

    def save_log(self):
        os.makedirs("historial", exist_ok=True)
        
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        log_file_name = f"{self.model_name.replace(' ', '_')}_{current_date}.log"
        log_path = os.path.join("historial", log_file_name)
        
        with open(log_path, "a") as f:
            for message in st.session_state.messages:
                f.write(f"{datetime.datetime.now()}: [{self.model_name}] {message['role']}: {message['content']}\n")