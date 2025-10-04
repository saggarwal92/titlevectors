from sentence_transformers import SentenceTransformer
from qdrant_client import models
from configs.configs import configs
    
class Vectorizer:
    _instance = None
    _initialized = False
    model: SentenceTransformer

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Vectorizer, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            model_name = configs.get_embedding_model_name()
            self.model = SentenceTransformer(model_name)
            self._initialized = True

    def get_vector_config(self):
        return models.VectorParams(
            size=self.model.get_sentence_embedding_dimension(), # type: ignore 
            distance=models.Distance.COSINE)

    def generate_embedding(self, text: str):
        return self.model.encode(text).tolist()
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of Vectorizer"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
