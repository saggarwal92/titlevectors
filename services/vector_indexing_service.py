from services.models import IndexableJobDocument
from storage.vectorizer import Vectorizer
from storage import vector_store
from qdrant_client import QdrantClient
from configs.configs import configs

class VectorIndexingService:
    __q_client: QdrantClient
    __vectorizer: Vectorizer

    def __init__(self):
        self.__q_client = QdrantClient(configs.get_qdrant_url())
        self.__vectorizer = Vectorizer(configs.get_embedding_model_name())

    def insert_documents(self, documents: list[IndexableJobDocument]):
        skill_vector_items = [self.__to_skills_vector_item(doc) for doc in documents]
        vector_store.insert_items(
            client = self.__q_client,
            collection_name = configs.get_skills_collection_name(),
            vectorizer = self.__vectorizer,
            items = skill_vector_items
        )

        res_vector_items = [self.__to_responsibilities_vector_item(doc) for doc in documents]
        vector_store.insert_items(
            client = self.__q_client,
            collection_name = configs.get_responsibilities_collection_name(),
            vectorizer = self.__vectorizer,
            items = res_vector_items
        )
    
    def __to_skills_vector_item(self, document: IndexableJobDocument) -> vector_store.VectorItem:
        return vector_store.VectorItem(
            item_id=document._get_document_id(),
            text=document._get_skills_vector_text(),
            metadata=document._get_payload()
        )

    def __to_responsibilities_vector_item(self, document: IndexableJobDocument):
        return vector_store.VectorItem(
            item_id=document._get_document_id(),
            text=document._get_responsibilities_vector_text(),
            metadata=document._get_payload()
        )
