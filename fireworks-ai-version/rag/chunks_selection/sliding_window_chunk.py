import sqlite3

class SlidingWindowChunkSelector:
    def __init__(self, db_path, window_size=300, stride=150):
        self.db_path = db_path
        self.window_size = window_size
        self.stride = stride
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    def get_all_chunks(self):
        self.cursor.execute("SELECT id, content, page_text_embedded FROM documents")
        all_chunks = []
        for row in self.cursor.fetchall():
            doc_id, content, embedding = row
            chunks = []
            for i in range(0, len(content) - self.window_size + 1, self.stride):
                chunk = content[i:i+self.window_size]
                chunks.append(chunk)
            for chunk in chunks:
                all_chunks.append({"doc_id": doc_id, "chunk": chunk, "page_text_embedded": embedding})
        return all_chunks