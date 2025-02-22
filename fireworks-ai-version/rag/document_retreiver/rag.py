class RAG_Handler:
    def __init__(self, retriever, chunk_selector, extract_template, embedding_model):
        self.retriever = retriever
        self.chunk_selector = chunk_selector
        self.extract_template = extract_template
        self.embedding_model = embedding_model

    def get_relevant_chunk_query(self, prompt, top_k=3):
        query_embedding = self.embedding_model.embed_query(prompt)
        relevant_chunks = self.retriever.get_most_relevant_chunks(query_embedding, top_k, self.chunk_selector)
        # Combinar los chunks relevantes en una sola cadena de texto
        chunks_text = "\n".join([chunk["chunk"] for _, chunk in relevant_chunks])
        return chunks_text

    def search_by_rag(self, prompt):
        query_embedding = self.embedding_model.embed_query(prompt)
        relevant_chunks = self.get_relevant_chunk_query(prompt, query_embedding)
        modified_template = self.extract_template.replace("{context}", relevant_chunks)
        modified_template = modified_template.replace("{query}", prompt)
        return modified_template
