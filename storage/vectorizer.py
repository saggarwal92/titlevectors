from sentence_transformers import SentenceTransformer
from qdrant_client import models
    
class Vectorizer:
    model: SentenceTransformer

    def __init__(self, model_name = 'BAAI/bge-base-en-v1.5'):
        self.model = SentenceTransformer(model_name)

    def get_vector_config(self):
        return models.VectorParams(
            size=self.model.get_sentence_embedding_dimension(), # type: ignore 
            distance=models.Distance.COSINE)

    def generate_embedding(self, text: str):
        return self.model.encode(text).tolist()
