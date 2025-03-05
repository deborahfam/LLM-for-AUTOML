from typing import List, Tuple
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.db.models import DocumentPageModel, DocumentMetadataModel
from services.db.mongodb import MongoDBService
from services.embeddings import EmbeddingService
import hashlib
from services.main import MainService
import pymupdf4llm
import pymupdf
import os
import dotenv

dotenv.load_dotenv()
db = os.getenv("DB_NAME")
collection = "document_page_table"

from prompts import (
    GENERATE_QUESTIONS,
    GENERATE_IDEAS,
    GENERATE_SUMMARIZE
)


class DocumentProcessorService:
    def __init__(self, embedding_model: EmbeddingService) -> None:
        self.embedding_model = embedding_model
        self.handler = MainService(embedding_model=embedding_model)
        self.model = "accounts/fireworks/models/mixtral-8x7b-instruct"
        self.recursive_text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=20
        )
        self.db_handler = MongoDBService()

    def embed_text(self, chunk_text: str):
        """Embed the chunk of text using the embedding model."""
        return self.embedding_model.embed_documents(chunk_text)

    def process_questions(self, chunk: str) -> Tuple[List[str], List[List[float]]]:
        """Generate questions and their embeddings."""
        questions = self.handler.generate_request_by_prompt(
            PROMPT=GENERATE_QUESTIONS, model=self.model, query=chunk
        )
        questions_embedded = self.embedding_model.embed_query(questions)
        return questions, questions_embedded

    def process_summary(self, text: str) -> Tuple[str, List[float]]:
        """Generate summary and its embedding."""
        summary = self.handler.generate_request_by_prompt(
            PROMPT=GENERATE_SUMMARIZE, model=self.model, query=text
        )
        summary_embedded = self.embedding_model.embed_query(summary)
        return summary, summary_embedded

    def process_principal_ideas(self, text: str) -> Tuple[List[str], List[List[float]]]:
        """Generate principal ideas and their embeddings."""
        principal_ideas = self.handler.generate_request_by_prompt(
            PROMPT=GENERATE_IDEAS, model=self.model, query=text
        )
        principal_ideas_embedded = self.embedding_model.embed_query(principal_ideas)
        return principal_ideas, principal_ideas_embedded

    def process_metadata(self, chunk):
        questions, questions_embedded = self.process_questions(chunk["text"])
        summary, summary_embedded = self.process_summary(chunk["text"])
        principal_ideas, principal_ideas_embedded = self.process_principal_ideas(
            chunk["text"]
        )
        metadata = DocumentMetadataModel(
            questions=questions,
            questions_embedded=questions_embedded,
            principal_ideas=principal_ideas,
            principal_ideas_embedded=principal_ideas_embedded,
            summarize=summary,
            summarize_embedded=summary_embedded,
        )
        metadata_id = self.db_handler.insert_one(
            "document_metadata_table", metadata.model_dump(by_alias=True)
        )
        return metadata_id

    def process_and_save(self, file):
        pdf_file = pymupdf.open(stream=file.read())
        md_text_chunks = pymupdf4llm.to_markdown(
            pdf_file, page_chunks=True, write_images=False
        )

        for chunk in md_text_chunks:
            print("isduplicate", self.is_duplicate(chunk["text"]), flush=True)
            if not self.is_duplicate(chunk["text"]):
                metadata_id = self.process_metadata(chunk)

                document_data = DocumentPageModel(
                    hash_code=hashlib.sha256(chunk["text"].encode("utf-8")).hexdigest(),
                    document_title=pdf_file.name,
                    document_name=pdf_file.name,  # TODO change this to the pdf path
                    total_pages=len(md_text_chunks),
                    page=chunk["metadata"]["page"],
                    page_text=chunk["text"],
                    page_text_embedded=self.embed_text(chunk["text"]),
                    metadata_id=metadata_id,
                )
                self.db_handler.insert_one(
                    "document_page_table", document_data.model_dump(by_alias=True)
                )

    def is_duplicate(self, text: str) -> bool:
        """Check if the text content already exists in the database."""
        hash_digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        existing_document = db["document_page_table"].find_one(
            {"hash_code": hash_digest}
        )
        return existing_document is not None

