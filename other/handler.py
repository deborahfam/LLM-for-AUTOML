from typing import List
from config import collection
from openai import OpenAI
import streamlit as st
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()
class LLMHandler:
    def __init__(self, embedding_model):
        self.embedding_model =  embedding_model
        
        self.client = OpenAI(
            base_url=os.getenv("OPENAI_API_BASE"), 
            api_key=os.getenv("OPENAI_API_KEY"))
        
    def get_response(self, query):
        #query_embedding = self.embedding_model.embed_documents(query)
        
        combined_input = (
            # f"The following is a relevant extract of a PDF document "
            # f"from which I will ask you a question.\n"
            # f"## Extract\n"
            f"{query}\n"
            # f"## Query\n"
            # f"Given the previous extract, answer the following query\n"
            # f"{query}"
        )

        return combined_input