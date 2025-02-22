import sqlite3
from document_retreiver.chunk_selector import FixedSizeChunkSelector, SlidingWindowChunkSelector  # Importar las estrategias
import numpy as np
from dotenv import load_dotenv

load_dotenv()

class Document_Retriever:
    def __init__(self, db_path):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_relevant_documents(self, query):
        self.cursor.execute("SELECT content FROM documents WHERE content LIKE ?", ('%' + query + '%',))
        return [row[0] for row in self.cursor.fetchall()]

    def get_most_relevant_chunks(self, query_embedding, top_k=3, chunk_selector=None):
        if chunk_selector is None:
            raise ValueError("chunk_selector must be an instance of a chunk selector class.")
        
        all_chunks = chunk_selector.get_all_chunks()
        similarities = []
        for chunk in all_chunks:
            embedded_vector = chunk["page_text_embedded"]
            similarity = np.dot(query_embedding, embedded_vector) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedded_vector)
            )
            similarities.append((similarity, chunk))
        sorted_chunks = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_k]
        return sorted_chunks