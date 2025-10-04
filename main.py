from fastapi import FastAPI
from routes.index_routes import router as index_router
from storage.vector_store import create_collection_if_not_exists
from qdrant_client import QdrantClient
from configs.configs import configs
from storage.vectorizer import Vectorizer
import logging

logging.basicConfig(level=logging.INFO)


# Create FastAPI app instance
app = FastAPI(
    title="Title Vectors API",
    description="A simple FastAPI application for document indexing and searching",
    version="1.0.0"
)

# Include routers
app.include_router(index_router, prefix="/similarity")


@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to Title Vectors API"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.on_event("startup")
async def startup_event():
    logging.error(f"Creating collections if they do not exist...: {configs.get_qdrant_url()}")
    client = QdrantClient(configs.get_qdrant_url())
    vectorizer = Vectorizer.get_instance()
    create_collection_if_not_exists(
        client = client,
        vectorizer = vectorizer,
        collection_name = configs.get_skills_collection_name()
    )
    create_collection_if_not_exists(
        client = client,
        vectorizer = vectorizer,
        collection_name = configs.get_responsibilities_collection_name()
    )
    logging.info("Collections are ready.")

if __name__ == "__main__":
    pass
    """python -m uvicorn main:app --reload --port 8000"""
