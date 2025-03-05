import os
import streamlit as st
from pymongo import MongoClient
from bson.objectid import ObjectId
from services.db.models import DocumentPageModel, DocumentMetadataModel
from dotenv import load_dotenv
from config import client, db

load_dotenv()

class MongoDBService:
    def __init__(self):
        self.client = client
        self.db = db

    def insert_one(self, collection_name: str, data: dict) -> str:
        return self.db[collection_name].insert_one(data).inserted_id

    def find_all(self, collection_name: str) -> list:
        return list(self.db[collection_name].find())

    def delete_one(self, collection_name: str, id: str) -> int:
        return self.db[collection_name].delete_one({"_id": ObjectId(id)}).deleted_count

    def find_by_param(self, collection_name: str, param: str, value) -> list:
        return list(self.db[collection_name].find({param: value}))

    def find_related(self, collection_name: str, param: str, id: str) -> dict:
        return self.db[collection_name].find_one({param: ObjectId(id)})

    def update_one(self, collection_name: str, id: str, update_data: dict) -> int:
        return (
            self.db[collection_name]
            .update_one({"_id": ObjectId(id)}, {"$set": update_data})
            .modified_count
        )

    def update_row(self, collection_name: str, id: str, row: str, new_value) -> int:
        return (
            self.db[collection_name]
            .update_one({"_id": ObjectId(id)}, {"$set": {row: new_value}})
            .modified_count
        )


class DocumentPage:
    def __init__(self, db_handler: MongoDBService):
        self.collection_name = "document_page_table"
        self.db_handler = db_handler

    def save(self, data: DocumentPageModel):
        """
        Save a document page to the database.
        """
        return self.db_handler.insert_one(
            self.collection_name, data.model_dump(by_alias=True)
        )

    def get_all(self):
        """
        Get all document pages from the database.
        """
        return self.db_handler.find_all(self.collection_name)

    def delete(self, id: str):
        """
        Delete a document page from the database by its ID.
        """
        return self.db_handler.delete_one(self.collection_name, id)

    def find_by(self, param: str, value: str):
        """
        Find document pages by a specific parameter.
        """
        return self.db_handler.find_by_param(self.collection_name, param, value)

    def get_related_metadata(self, metadata_id: str):
        """
        Get related metadata for a document page by its metadata ID.
        """
        return self.db_handler.find_related(
            "document_metadata_table", "_id", metadata_id
        )

    def update(self, id: str, update_data: DocumentPageModel):
        """
        Update a document page in the database by its ID.
        """
        return self.db_handler.update_one(
            self.collection_name, id, update_data.model_dump(by_alias=True)
        )

    def update_row(self, id: str, row: str, new_value):
        """
        Update a specific row of a document page in the database by its ID.
        """
        return self.db_handler.update_row(self.collection_name, id, row, new_value)


class DocumentMetadata:
    def __init__(self, db_handler: MongoDBService):
        self.collection_name = "document_metadata_table"
        self.db_handler = db_handler

    def save(self, data: DocumentMetadataModel):
        """
        Save document metadata to the database.
        """
        return self.db_handler.insert_one(
            self.collection_name, data.model_dump(by_alias=True)
        )

    def get_all(self):
        """
        Get all document metadata from the database.
        """
        return self.db_handler.find_all(self.collection_name)

    def delete(self, id: str):
        """
        Delete document metadata from the database by its ID.
        """
        return self.db_handler.delete_one(self.collection_name, id)

    def find_by(self, param: str, value: str):
        """
        Find document metadata by a specific parameter.
        """
        return self.db_handler.find_by_param(self.collection_name, param, value)

    def update(self, id: str, update_data: DocumentMetadataModel):
        """
        Update document metadata in the database by its ID.
        """
        return self.db_handler.update_one(
            self.collection_name, id, update_data.model_dump(by_alias=True)
        )

    def update_row(self, id: str, row: str, new_value):
        """
        Update a specific row of document metadata in the database by its ID.
        """
        return self.db_handler.update_row(self.collection_name, id, row, new_value)