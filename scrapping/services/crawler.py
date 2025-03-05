import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from services.main import MainService
from dotenv import load_dotenv
import os
import streamlit as st
from config import collection

load_dotenv()

class CrawlerService:
    def __init__(self, embedding_model) -> None:
        self.visited = set()
        self.embedding_model = embedding_model
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=20
        )
        # self.stop_words = set(stopwords.words("english"))
        # self.stemmer = PorterStemmer()
        # self.lemmatizer = WordNetLemmatizer()
        self.handler = MainService(embedding_model=embedding_model)
        print(f"handler pase por el init del crawler service", self.handler )

    # def preprocess_text(self, text):
    #     """Preprocess the text by removing stop words, stemming, and lemmatizing."""
    #     tokens = nltk.word_tokenize(text)
    #     tokens = [word for word in tokens if word.lower() not in self.stop_words]
    #     return " ".join(tokens)

    def crawl(self, start_url, max_depth, max_links_per_page=2):
        queue = [(start_url, 0)]

        while queue:
            url, depth = queue.pop(0)
            if depth > max_depth or url in self.visited:
                continue

            try:
                print(f"Crawling URL: {url} at depth {depth}")
                response = requests.get(url)
                print(f"response status code: {response.status_code}")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    text = (
                        soup.get_text()
                        .replace("\n", " ")
                        .replace(".", "")
                        .replace("-", "")
                    )
                    # file_processed = self.preprocess_text(text)
                    file_processed = text
                    # Process and embed the text in chunks
                    chunks = self.recursive_text_splitter.create_documents(
                        [file_processed]
                    )
                    st.write("crawler processer chunks", chunks)

                    for chunk in chunks:
                        chunk_text = chunk.page_content
                        chunk_text_embedded = self.embedding_model.embed_documents(chunk_text)
                        self.save_to_db(
                            url, chunk_text, chunk_text_embedded
                        )

                    self.visited.add(url)

                    links = soup.find_all("a")
                    num_links = 0
                    for link in links:
                        child_url = link.get("href")
                        if (
                            child_url
                            and child_url.startswith("http")
                            and num_links < max_links_per_page
                        ):
                            queue.append((child_url, depth + 1))
                            num_links += 1
            except Exception as e:
                with open("debug.log", "a") as w:
                    w.write(f"Error crawling {url}: {str(e)}\n")

    def save_to_db(self, url, text_data, embedded_vector):
        data = {
            "name": url,
            "chunk_text": text_data,
            "embedded_vector": embedded_vector,
        }
        collection.insert_one(data)
