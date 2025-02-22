from typing import List, Union
import dotenv
import os
from openai import OpenAI

dotenv.load_dotenv()

class Embedding_Service:
    def __init__(self, model):
        self.model = model
        
        self.client = OpenAI(
            base_url=os.getenv("FIREWORKS_API_BASE"), 
            api_key=os.getenv("FIREWORKS_API_KEY"))

    def get_embedding(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding

    def embed_documents(self, text) -> List[List[float]]:
        return self.get_embedding(text)

    def embed_query(self, text: str) -> List[float]:
        return self.get_embedding(text)

    def embed_image(self, image_path: str) -> List[float]:
        return self.get_embedding(image_path, model="image-embedding-model")

    def embed_table(self, table_data: List[str]) -> List[float]:
        return self.get_embedding(table_data, model="table-embedding-model")

    def multi_embed(
        self, content_items: List[Union[str, List[str]]], models: List[str]
    ) -> List[List[float]]:
        embeddings = []
        for content, model in zip(content_items, models):
            embeddings.append(self.get_embedding(content, model))
        return embeddings
