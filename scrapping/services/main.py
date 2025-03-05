import json
from typing import List
from openai import OpenAI
import streamlit as st
import numpy as np
import os
from dotenv import load_dotenv
from prompts import (
    GENERATE_SUMMARIZE,
    IMAGE_TEMPLATE,
    RAG_WITH_FEEDBACK_TEMPLATE,
    RAG_TEMPLATE,
    SIMILITUDE_PROMPT,
)
import re
from config import collection, db

load_dotenv()


class MainService:
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

        self.client = OpenAI(
            base_url=os.getenv("FIREWORKS_API_BASE"), 
            api_key=os.getenv("FIREWORKS_API_KEY"))

        self.user_prompt = ""
        self.system_prompt = "You are an assistant bot and modify the way to respond to be polite and nice"

    def get_most_relevant_chunks(self, query_embedding: List[float], top_k: int = 3):
        all_documents = list(db["document_page_table"].find())
        similarities = []

        for doc in all_documents:
            embedded_vector = doc["page_text_embedded"]
            similarity = np.dot(query_embedding, embedded_vector) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedded_vector)
            )
            similarities.append((similarity, doc))

        sorted_docs = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_k]
        return sorted_docs

    def get_most_relevant_chunks_with_links(self, query: str, top_k: int = 1):
        all_documents = list(db["video_description_table"].find())
        query_embedding = self.embedding_model.embed_documents(query)
        similarities = []

        for doc in all_documents:
            embedded_vector = doc["page_text_embedded"]
            similarity = np.dot(query_embedding, embedded_vector) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedded_vector)
            )
            similarities.append((similarity, doc))

        sorted_docs = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_k]
        return sorted_docs

    def get_most_relevant_questions(self, query_embedding: List[float], top_k: int = 3):
        all_metadata = list(db["document_metadata_table"].find())
        similarities = []

        for meta in all_metadata:
            embedded_vector = meta["questions_embedded"]
            similarity = np.dot(query_embedding, embedded_vector) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(embedded_vector)
            )
            similarities.append((similarity, meta))

        sorted_docs = sorted(similarities, key=lambda x: x[0], reverse=True)[:top_k]
        sorted_metadata = [doc[1] for doc in sorted_docs]
        return sorted_metadata

    def get_relevant_chunk_query(self, query):
        query_embedding = self.embedding_model.embed_documents(query)
        most_relevant_docs = self.get_most_relevant_chunks(query_embedding)
        context = "\n\n".join(doc["page_text"] for _, doc in most_relevant_docs)
        return context

    def get_response(self, query):
        query_embedding = self.embedding_model.embed_documents(query)
        most_relevant_docs = self.get_most_relevant_chunks(query_embedding)
        context = "\n\n".join(doc["page_text"] for _, doc in most_relevant_docs)
        combined_input = RAG_TEMPLATE.replace("{context}", context)
        combined_input = combined_input.replace("{query}", query)
        return combined_input

    def search_by_rag(self, prompt):
        relevants_chunks = self.get_relevant_chunk_query(prompt)
        template: str = st.session_state["extract_template"]
        modified_template = template.replace("{context}", relevants_chunks)
        modified_template = modified_template.replace("{query}", prompt)
        return modified_template

    def get_relevant_chunck_query_with_images(self, query):
        query_embedding = self.embedding_model.embed_documents(query)
        most_relevant_docs = self.get_most_relevant_chunks(query_embedding)
        context = []
        for _, doc in most_relevant_docs:
            context.append(doc["page_text"])
        images = self.image_handler.get_images_from_chunks(most_relevant_docs)
        return context, images

    def search_by_rag_with_images(self, prompt, model):
        if model == "gpt-4o":
            relevants_chunks, images = self.get_relevant_chunck_query_with_images(
                prompt
            )
            template = IMAGE_TEMPLATE
            relevants_chunks = list(relevants_chunks)  # Convert generator to list
            for idx, chunk in enumerate(relevants_chunks):
                template = template.replace("{context" + str(idx) + "}", chunk)
            template = template.replace("{query}", prompt)
            response = self.submit_to_chatGPT(template, model)
            return template, response, images
        else:
            relevants_chunks, images = self.get_relevant_chunck_query_with_images(
                prompt
            )
            template = IMAGE_TEMPLATE
            relevants_chunks = list(relevants_chunks)  # Convert generator to list
            for idx, chunk in enumerate(relevants_chunks):
                template = template.replace("{context" + str(idx) + "}", chunk)
            template = template.replace("{query}", prompt)
            response = self.submit_to_llm(template, model)
            # Add to the response a last line adding the link obtained from the method get_most_relevant_chunks_with_links
            video_links = self.retribute_video_links(prompt, model)
            if video_links != "":
                # Add the link with the frase "If you need more information, check the following video link"
                response += f"\n\nIf you need more information, check the following video link: [{video_links[0]}"
            return template, response, images

    def retribute_video_links(self, prompt, model):
        most_relevant_doc = self.get_most_relevant_chunks_with_links(prompt)

        if not most_relevant_doc:
            return ""

        prompt_template = SIMILITUDE_PROMPT.replace(
            "{context}", most_relevant_doc[0][1]["page_text"]
        )
        prompt_template = prompt_template.replace("{transcription}", prompt)
        response = self.submit_to_llm(prompt_template, model, jsonVar=True)
        # Response is a JSON object
        video_links = ""
        if response["classification"] == "Yes":
            # Obtain the video links by a regex expression
            video_links = re.findall(
                r"https?://\S+", most_relevant_doc[0][1]["page_text"]
            )
        return video_links

    def llm_guided_search(self, prompt):
        query_embedding = self.embedding_model.embed_documents(prompt)
        relevants_chunks = self.get_relevant_chunk_query(prompt)
        q_related_chunks = self.get_most_relevant_questions(query_embedding, 1)
        prompt_template = "The following texts contains questions and usefull information of the questions related with the query introduced by the user"

        for idx, item in enumerate(q_related_chunks):
            prompt_template += (
                f"##QUESTIONS {item['questions']}\n"
                f"The following information is related to the answer of the question before: "
                + f"{item['summarize']}\n\n"
            )

        prompt_template += f"The following context is information related with the user query ##CONTEXT {relevants_chunks}. Given all the information that I just give you, answer the followint query ##QUERY {prompt}"
        return prompt_template

    def search_by_rag_with_feedback(self, prompt, model):
        prompt_modified = self.search_by_rag(prompt)
        response = self.submit_to_llm(prompt_modified, model)
        new_prompt_template = RAG_WITH_FEEDBACK_TEMPLATE.replace("{text}", response)
        new_prompt_template = new_prompt_template.replace("{query}", prompt)
        return new_prompt_template

    def submit_to_llm(self, prompt, llm, jsonVar=False):
        if jsonVar:
            return json.loads(
                self.client.chat.completions.create(
                    model=llm,
                    messages=[{"role": "user", "content": prompt}],
                    stream=False,
                    response_format=dict(type="json_object"),
                )
                .choices[0]
                .message.content
            )
        else:
            response = self.client.chat.completions.create(
                model=llm,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
            )
            return response.choices[0].message.content

    def generate_request_by_prompt(self, PROMPT: str, model: str, query: str):
        prompt = PROMPT.replace("{query}", query)
        response = self.submit_to_llm(prompt=prompt, llm=model)
        return response

    def generate_caption(self, PROMPT: str, model: str, text: str, image_text: str):
        prompt = PROMPT.replace("{query}", text)
        prompt = prompt.replace("{image_text}", image_text)
        response = self.submit_to_llm(prompt=prompt, llm=model, jsonVar=True)
        return response

    def parse_json(self, prompt, model):
        messages = [{"role": "user", "content": prompt}]
        client = self.client
        return json.loads(
            client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False,
                response_format=dict(type="json_object"),
            )
            .choices[0]
            .message.content
        )
