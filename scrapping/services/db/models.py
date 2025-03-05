from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional


class DocumentPageModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    hash_code: str
    document_title: str
    document_name: str
    total_pages: int
    page: int
    page_text: str
    metadata_id: str
    page_text_embedded: List[float]

    class Config:
        allow_population_by_field_name = True


class DocumentMetadataModel(BaseModel):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    questions: str
    principal_ideas: str
    summarize: str
    questions_embedded: List[float]
    principal_ideas_embedded: List[float]
    summarize_embedded: List[float]

    class Config:
        allow_population_by_field_name = True



# TODO: Move this functions to MongoDBService


def save_document_page(db_handler, data):
    document_page = DocumentPageModel(**data)
    return db_handler.insert_one(
        "document_page_table", document_page.model_dump(by_alias=True)
    )


def save_document_metadata(db_handler, data):
    document_metadata = DocumentMetadataModel(**data)
    return db_handler.insert_one(
        "document_metadata_table", document_metadata.model_dump(by_alias=True)
    )