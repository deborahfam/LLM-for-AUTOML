import requests, os
from dotenv import load_dotenv
from openai import OpenAI
from model_config import MODEL_CONFIGURATIONS
from services.message_history import Message_Handler
load_dotenv()

class Client_Handler:
    def __init__(self):
        # self.embedding_model =  embedding_model
        self.model = MODEL_CONFIGURATIONS["DeepSeek R1"]
        self.context_handler = Message_Handler(self.model)
        
        self.client = OpenAI(
            base_url=os.getenv("FIREWORKS_API_BASE"), 
            api_key=os.getenv("FIREWORKS_API_KEY"))

    def submit_to_llm(self):
        response = self.client.chat.completions.create(
            model= self.model["model_name"],
            messages= self.context_handler.get_context(),
            stream=False,
            temperature=0.7
        );
        return response.choices[0].message.content