from services.document_retriever import DocumentRetriever
from openai import OpenAI
import os
from dotenv import load_dotenv
from .clustering.clustering_algorithm import ClusteringAlgorithm
from .clustering.cluster_selector import ClusterSelector

load_dotenv()

class DynamicClusteringRAG:
    def __init__(self, model_name, db_path, n_clusters=5):
        self.client = OpenAI(
            base_url=os.getenv("FIREWORKS_API_BASE"), 
            api_key=os.getenv("FIREWORKS_API_KEY")
        )
        self.model_name = model_name
        self.document_retriever = DocumentRetriever(db_path)
        self.clustering_algorithm = ClusteringAlgorithm(n_clusters)
        self.cluster_selector = ClusterSelector(self.clustering_algorithm)

    def generate_response_with_clustering(self, user_query):
        relevant_documents = self.document_retriever.get_relevant_documents(user_query)
        embeddings = [self.document_retriever.get_embedding(doc) for doc in relevant_documents]  # Asumiendo que hay un método para obtener embeddings

        representative_docs = self.cluster_selector.select_representative_documents(relevant_documents, embeddings)
        context = "\n".join(representative_docs)
        prompt = f"Based on the following information, answer the question:\n{context}\nQuestion: {user_query}"

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content

    def close(self):
        self.document_retriever.close()