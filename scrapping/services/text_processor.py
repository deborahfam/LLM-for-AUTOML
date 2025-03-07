from langchain_text_splitters import RecursiveCharacterTextSplitter
import streamlit as st

# text_processor.py actualizado
class TextProcessor:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
        self._init_ui()

    def _init_ui(self):
        st.sidebar.subheader("Procesamiento de Texto")
        self.token_counter = st.sidebar.empty()

    def process_text(self, text: str):
        try:
            with st.spinner("Procesando texto..."):
                # Fase 1: Limpieza
                try:
                    cleaned_text = self._clean_text(text)
                except Exception as e:
                    raise Exception(f"Error en limpieza de texto: {str(e)}") from e
                
                # Fase 2: Segmentación
                try:
                    chunks = self._split_text(cleaned_text)
                except Exception as e:
                    raise Exception(f"Error en división de texto: {str(e)}") from e
                
                # Fase 3: Generación de embeddings
                try:
                    processed_chunks = self._generate_embeddings(chunks)
                    return chunks, processed_chunks
                except Exception as e:
                    raise Exception(f"Error generando embeddings: {str(e)}") from e
                    
        except Exception as e:
            st.error(f"Error en procesamiento de texto: {str(e)}")
            raise

    def _clean_text(self, text: str) -> str:
        return text.replace("\n", " ").replace(".", "").replace("-", "")

    def _split_text(self, text: str):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=20,
            length_function=len,
            separators=["\n\n", "\. ", "\n", " ", ""],
            keep_separator=True
        )
        return splitter.create_documents([text])

    def _generate_embeddings(self, chunks):
        embeddings = []
        progress_bar = st.progress(0)
        for i, chunk in enumerate(chunks):
            st.write("chunk ", chunks)
            chunk_text = chunk.page_content
            chunk_embed = self.embedding_model.embed_documents(chunk_text)
            embeddings.append(chunk_embed)
            progress_bar.progress((i + 1) / len(chunks))
            self.token_counter.write(f"Tokens procesados: {(i + 1) * 2000}")
        
        return embeddings