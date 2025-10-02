from dataclasses import dataclass
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from storage.vectorizer import Vectorizer
import logging

@dataclass
class VectorItem:
    item_id: str
    text: str
    metadata: dict

def create_collection_if_not_exists(
        client: QdrantClient, 
        vectorizer: Vectorizer, 
        collection_name: str):
    """Create a Qdrant collection if it does not already exist"""
    existing_collections = client.get_collections().collections
    if any(col.name == collection_name for col in existing_collections):
        logging.info(f"Collection '{collection_name}' already exists.")
        return  # Collection already exists
    logging.info(f"Creating collection '{collection_name}'.")
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config={"default": vectorizer.get_vector_config()}
    )

def insert_items(
        client: QdrantClient, 
        collection_name: str, 
        vectorizer: Vectorizer, 
        items: list[VectorItem]):
    """Insert an item into the specified Qdrant collection"""
    points = [
        PointStruct(
            id = item.item_id,
            vector = {"default": vectorizer.generate_embedding(item.text)},
            payload = item.metadata
        )
        for item in items
    ]

    client.upsert(
        collection_name=collection_name,
        points=points
    )

def search_items(
        client: QdrantClient, 
        collection_name: str, 
        vectorizer: Vectorizer, 
        query_text: str, 
        top_k: int,
        score_threshold: float = 0.8) -> list[dict]: 
    """
        Search for items in the specified Qdrant collection.

        Example output:
        [
            {
                "id": "538bb680-3272-5c2b-bb73-f9dbe1fc292e",
                "score": 0.82117903,
                "payload": {
                "titles": [
                    "Solutions Consultant",
                    "Advertising Solutions Consultant"
                ],
                "job_id": "68cfa0c0d13d747f4c34f4e6"
                }
            },
            {
                "id": "1f5cb9cb-bf4f-5d2b-a700-6cca4c06b1fb",
                "score": 0.80463666,
                "payload": {
                "titles": [
                    "Software Engineering Intern",
                    "Web Development Intern"
                ],
                "job_id": "68bd7923808b484560386fa2"
                }
            }
        ]
    """
    
    query_vector = vectorizer.generate_embedding(query_text)
    results = client.search(
        collection_name=collection_name,
        query_vector=("default", query_vector),
        limit=top_k,
        score_threshold=score_threshold
    )
    return [
        {
            "id": result.id,
            "score": result.score,
            "payload": result.payload
        }
        for result in results
    ]