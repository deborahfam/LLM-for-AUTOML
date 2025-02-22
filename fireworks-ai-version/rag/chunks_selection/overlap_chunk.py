import sqlite3

class OverlapChunkSelector:
    def __init__(self, db_path, chunk_size=500, overlap_size=100):
        self.db_path = db_path
        self.chunk_size = chunk_size
        self.overlap_size = overlap_size
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_all_chunks(self):
        self.cursor.execute("SELECT id, content, page_text_embedded FROM documents")
        all_chunks = []
        for row in self.cursor.fetchall():
            doc_id, content, embedding = row
            chunks = []
            for i in range(0, len(content) - self.chunk_size + 1, self.chunk_size - self.overlap_size):
                chunk = content[i:i+self.chunk_size]
                chunks.append(chunk)
            for chunk in chunks:
                all_chunks.append({"doc_id": doc_id, "chunk": chunk, "page_text_embedded": embedding})
        return all_chunks