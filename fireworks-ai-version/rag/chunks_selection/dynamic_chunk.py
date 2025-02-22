import sqlite3

class DynamicChunkSelector:
    def __init__(self, db_path, min_chunk_size=100, max_chunk_size=500):
        self.db_path = db_path
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_all_chunks(self):
        self.cursor.execute("SELECT id, content, page_text_embedded FROM documents")
        all_chunks = []
        for row in self.cursor.fetchall():
            doc_id, content, embedding = row
            # Lógica para determinar el tamaño del chunk dinámicamente
            chunk_size = min(max(len(content) // 10, self.min_chunk_size), self.max_chunk_size)
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            for chunk in chunks:
                all_chunks.append({"doc_id": doc_id, "chunk": chunk, "page_text_embedded": embedding})
        return all_chunks