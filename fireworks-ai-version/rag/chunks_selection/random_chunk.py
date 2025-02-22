import sqlite3
import random

class RandomChunkSelector:
    def __init__(self, db_path, num_chunks=5):
        self.db_path = db_path
        self.num_chunks = num_chunks
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_all_chunks(self):
        self.cursor.execute("SELECT id, content, page_text_embedded FROM documents")
        all_chunks = []
        rows = self.cursor.fetchall()
        selected_rows = random.sample(rows, min(self.num_chunks, len(rows)))
        for row in selected_rows:
            doc_id, content, embedding = row
            all_chunks.append({"doc_id": doc_id, "chunk": content, "page_text_embedded": embedding})
        return all_chunks