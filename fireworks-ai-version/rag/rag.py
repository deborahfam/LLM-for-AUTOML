from openai import OpenAI
from services.document_retriever import DocumentRetriever
import os
from dotenv import load_dotenv

load_dotenv()

class RAG:
    def __init__(self, model_name, db_path):
        self.client = OpenAI(
            base_url=os.getenv("FIREWORKS_API_BASE"), 
            api_key=os.getenv("FIREWORKS_API_KEY"))
        self.model_name = model_name
        self.document_retriever = DocumentRetriever(db_path)

    def generate_response(self, user_query):
        relevant_documents = self.document_retriever.get_relevant_documents(user_query)
        
        # Combinar la consulta del usuario con los documentos recuperados
        context = "\n".join(relevant_documents)
        prompt = f"Based on the following information, answer the question:\n{context}\nQuestion: {user_query}"

        # Generar respuesta utilizando el modelo
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    def close(self):
        self.document_retriever.close()