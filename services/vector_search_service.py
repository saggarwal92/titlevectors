from services.models import SearchableJobDocument, SearchResult
from storage.vectorizer import Vectorizer
from storage import vector_store
from qdrant_client import QdrantClient
from configs.configs import configs
import logging

class VectorSearchService:
    __q_client: QdrantClient
    __vectorizer: Vectorizer

    def __init__(self):
        self.__q_client = QdrantClient(configs.get_qdrant_url())
        self.__vectorizer = Vectorizer(configs.get_embedding_model_name())

    def search_items(self, document: SearchableJobDocument):
        skill_suggestions = self.__get_skill_based_suggestions(document)
        responsibilities_suggestions = self.__get_responsibility_based_suggestions(document)

        if len(skill_suggestions) == 0 or len(responsibilities_suggestions) == 0:
            logging.warning("No suggestions found for the given document.")
            return []
        
        return self.__get_merged_suggestions(skill_suggestions, responsibilities_suggestions)
    

    def __get_skill_based_suggestions(self, document: SearchableJobDocument) -> list[SearchResult]:
        skills_text = document._get_skills_vector_text()
        results = vector_store.search_items(
            client = self.__q_client,
            collection_name=configs.get_skills_collection_name(),
            vectorizer= self.__vectorizer,
            query_text=skills_text,
            top_k=5
        )
        skill_suggestions = [SearchResult(res) for res in results]
        return skill_suggestions
    
    def __get_responsibility_based_suggestions(self, document: SearchableJobDocument) -> list[SearchResult]:
        responsibilities_text = document._get_responsibilities_vector_text()
        results = vector_store.search_items(
            client = self.__q_client,
            collection_name=configs.get_responsibilities_collection_name(),
            vectorizer= self.__vectorizer,
            query_text=responsibilities_text,
            top_k=5
        )
        responsibility_suggestions = [SearchResult(res) for res in results]
        return responsibility_suggestions

    def __get_merged_suggestions(self, skill_results: list[SearchResult], res_results: list[SearchResult]):
        skill_suggestions = self.__extract_unique_suggestions(skill_results)
        responsibility_suggestions = self.__extract_unique_suggestions(res_results)

        # intersection titles
        merged_suggestions = []
        for title in skill_suggestions:
            if title in responsibility_suggestions:
                confidence_score = skill_suggestions[title]['score'] + responsibility_suggestions[title]['score']
                match_job_ids = list(
                    skill_suggestions[title]['match_job_ids'].union(
                        responsibility_suggestions[title]['match_job_ids'])
                )
                merged_suggestions.append({
                    'suggestion_source': 'both',
                    'title': title,
                    'score': confidence_score,
                    'match_job_ids': match_job_ids
                })
        return merged_suggestions
    
    def __extract_unique_suggestions(self, results: list[SearchResult]) -> dict:
        if len(results) == 0:
            return {}
        results = sorted(results, key=lambda x: x.score, reverse=True)

        unique_suggestions = {}
        for match_result in results:
            for title in match_result.titles:
                if title in unique_suggestions:
                    continue
                unique_suggestions[title] = {
                    # reduce score since it's from one index only
                    'score': match_result.score * 0.5,
                    'match_job_ids': {match_result.job_id}
                }

        return unique_suggestions

"""
def __extract_only_repeated_suggestions(results: list[dict], suggestion_source: str) -> list[dict]:
    if len(results) < 3:
        return []
    results = sorted(results, key=lambda x: x['confidence'], reverse=True)

    suggested_titles = results[0]['suggested_titles']
    # Get count and sum of confidence score for each title in suggested_titles
    title_score = {}
    for title in suggested_titles:
        title_score[title] = {
            'count': 0,
            'confidence': 0,
            'match_job_ids': set()
        }
        for match_result in results:
            if title in match_result['suggested_titles']:
                title_score[title]['count'] += 1
                title_score[title]['confidence'] += match_result['confidence']
                title_score[title]['match_job_ids'].add(match_result['job_id'])
    
    # Normalize confidence score by total result count
    total_results = len(results)
    for title in title_score:
        title_score[title]['confidence'] = title_score[title]['confidence'] / total_results
    
    # Filter titles that have confidence score > 0.85 and count > 2
    filtered_titles = []
    for title in title_score:
        if title_score[title]['confidence'] > 0.85 and title_score[title]['count'] > 2:
            filtered_titles.append({
                'suggestion_source': suggestion_source,
                'title': title,
                'confidence': title_score[title]['confidence'],
                'match_job_ids': list(title_score[title]['match_job_ids'])
            })
    return filtered_titles
"""