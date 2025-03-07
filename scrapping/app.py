import streamlit as st
import os, dotenv
from services.db.mongodb import MongoDBService
from services.text_processor import TextProcessor
from services.crawler import CrawlerService
from services.embeddings import EmbeddingService
from services.doc_processor import DocumentProcessorService

dotenv.load_dotenv()
st.set_page_config(page_title="Chatbot - Crawler", page_icon="💬", layout="wide")
embedding_model = (EmbeddingService()) 
db_service = MongoDBService()
text_processor = TextProcessor(embedding_model)
crawler = CrawlerService(db_service, text_processor)

def doc():
        st.title("Document Processor")

        st.subheader("Upload a Document")
        uploaded_files = st.file_uploader(
            "Choose files", type=["txt", "pdf"], accept_multiple_files=True
        )

        if uploaded_files:
            embedding_model = EmbeddingService()
            processor = DocumentProcessorService(embedding_model)

            for uploaded_file in uploaded_files:
                with st.spinner(f"Crawling PDF: {uploaded_file.name}"):
                    processor.process_and_save(uploaded_file)
                st.write("Crawling completed.")

def web():
        st.title("Web Crawler with Embeddings")

        # input_method = st.selectbox(
        #     "Select input method",
        #     ["Single URL", "Multiple URLs", "Upload text file with URLs"],
        # )
        input_method = 'Single URL'

        urls = []
        if input_method == "Single URL":
            url = st.text_input("Enter URL")
            if url:
                urls.append(url)
        elif input_method == "Multiple URLs":
            urls_input = st.text_area("Enter multiple URLs (one per line)")
            if urls_input:
                urls = urls_input.splitlines()
        elif input_method == "Upload text file with URLs":
            uploaded_file = st.file_uploader("Choose a file")
            if uploaded_file is not None:
                urls = [
                    line.decode("utf-8").strip() for line in uploaded_file.readlines()
                ]

        # max_depth = st.number_input("Max Depth", min_value=1, max_value=10, value=2)
        max_depth = 2

        col1, col2,col3 = st.columns([1, 0.5, 8])
        with col1:
            start_crawling = st.button("Start Crawling")
        with col2:
            reset = st.button("Reset")
        with col3:
             pass

        if reset:
            st.rerun()

        if start_crawling:
            if urls:
                try:
                    crawler = CrawlerService(
                         database_service=db_service, 
                         text_processor=text_processor, 
                         embedding_model=embedding_model
                    )
                    for url in urls:
                        with st.spinner(f"Crawling URL: {url}"):
                            crawler.crawl(url, max_depth)
                        st.write("Crawling completed.")
                except Exception as e:
                    st.error(f"Error during crawling: {e}")
            else:
                st.error("Please enter a valid URL.")

def main():
        # doc_tab, web_tab = st.tabs(["📚 Document Parser", "🌐 Website Crawler"])

        # with web_tab:
        #     web()
        # with doc_tab:
        #     doc()

    # Interfaz de usuario
    st.title("Sistema de Web Crawling Inteligente")
    url = st.text_input("URL inicial", "https://example.com")
    depth = st.slider("Profundidad máxima", 1, 5, 2)

    if st.button("Iniciar Crawling"):
        crawler.crawl(start_url=url, max_depth=depth)

if __name__ == "__main__":
        main()
