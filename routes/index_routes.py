from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services.vector_search_service import VectorSearchService
from services.vector_indexing_service import VectorIndexingService
from services.models import IndexableJobDocument, SearchableJobDocument
import logging

router = APIRouter()

vector_indexing_service = VectorIndexingService()
vector_search_service = VectorSearchService()

@router.post("/api/index")
async def indexing_api(request: Request):
    json_data = await request.json()
    jobs = json_data['jobs']
    documents = []
    for job in jobs:
        documents.append(
            IndexableJobDocument(
                job_id=job["job_id"],
                company_slug=job["company_slug"],
                llm_primary_title=job["llm_primary_title"],
                llm_secondary_title=job["llm_secondary_title"],
                short_description=job["short_description"],
                llm_responsibilities=job["llm_responsibilities"],
                llm_skills=job["llm_skills"],
                selected_titles=job["selected_titles"],
                hop_level=job["hop_level"],
                source=job["source"]
            )
        )
    vector_indexing_service.insert_documents(documents)
    return JSONResponse(content={"success": True})


@router.post("/api/suggest")
async def suggestions_api(request: Request):
    json_data = await request.json()
    document = SearchableJobDocument(
        company_slug=json_data["company_slug"],
        llm_primary_title=json_data["llm_primary_title"],
        llm_secondary_title=json_data["llm_secondary_title"],
        short_description=json_data["short_description"],
        llm_responsibilities=json_data["llm_responsibilities"],
        llm_skills=json_data["llm_skills"],
    )
    suggestions = vector_search_service.search_items(document)
    logging.info(f"Suggestions: {suggestions}")
    return JSONResponse(content=suggestions)