from services.document_retriever import DocumentRetriever
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class ActiveRefinementRAG:
    def __init__(self, model_name, db_path):
        self.client = OpenAI(
            base_url=os.getenv("FIREWORKS_API_BASE"), 
            api_key=os.getenv("FIREWORKS_API_KEY")
        )
        self.model_name = model_name
        self.document_retriever = DocumentRetriever(db_path)

    def generate_response_with_refinement(self, user_query):
        relevant_documents = self.document_retriever.get_relevant_documents(user_query)
        context = "\n".join(relevant_documents)
        prompt = f"Based on the following information, answer the question:\n{context}\nQuestion: {user_query}"

        # Generar respuesta inicial
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        answer = response.choices[0].message.content

        # Solicitar retroalimentación
        feedback_prompt = f"Initial answer: {answer}\nIs this answer satisfactory? If not, please provide feedback."
        feedback_response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": feedback_prompt}],
            temperature=0.7
        )
        feedback = feedback_response.choices[0].message.content

        # Refinar respuesta si es necesario
        if "no" in feedback.lower():
            refined_prompt = f"Refine the following answer based on this feedback: {feedback}\nAnswer: {answer}"
            refined_response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": refined_prompt}],
                temperature=0.7
            )
            return refined_response.choices[0].message.content

        return answer

    def close(self):
        self.document_retriever.close()