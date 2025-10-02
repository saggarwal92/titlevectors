
class Configs:
    __QDRANT_URL: str
    __EMBEDDING_MODEL_NAME: str
    __SKILLS_COLLECTION_NAME: str
    __RESPONSIBILITIES_COLLECTION_NAME: str

    def __init__(self):
        self.__SKILLS_COLLECTION_NAME = "desc_skills"
        self.__RESPONSIBILITIES_COLLECTION_NAME = "desc_res"
        self.__EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
        self.__load_dev_config()

    def __load_dev_config(self):
        self.__QDRANT_URL = "http://72.60.201.38:6333"
    
    def __load_prod_config(self):
        self.__QDRANT_URL = "http://localhost:6333"
    
    def get_qdrant_url(self):
        return self.__QDRANT_URL
    
    def get_embedding_model_name(self):
        return self.__EMBEDDING_MODEL_NAME
    
    def get_skills_collection_name(self):
        return self.__SKILLS_COLLECTION_NAME
    
    def get_responsibilities_collection_name(self):
        return self.__RESPONSIBILITIES_COLLECTION_NAME

configs = Configs()