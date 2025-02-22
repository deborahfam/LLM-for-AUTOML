from typing import List
from openai import OpenAI
from langchain_core.embeddings import Embeddings

def initialize_client(base_url: str):
    return OpenAI(base_url=base_url, api_key="tom")

#client = initialize_client(base_url="http://172.18.0.2:8000/v1")

client = OpenAI(base_url="http://172.20.0.2:8000/v1", api_key="lm-studio")

def get_embedding(text: str, model: str = "nomic-ai/nomic-embed-text-v1.5-GGUF") -> List[float]:
    return client.embeddings.create(input=[text], model=model).data[0].embedding

class LMStudioEmbedding(Embeddings):
    def embed_query(self, text: str) -> List[float]:
        return get_embedding(text)