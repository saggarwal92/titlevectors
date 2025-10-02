from dataclasses import dataclass
import uuid

@dataclass
class BaseJobDocument:
    company_slug: str
    llm_primary_title: str
    llm_secondary_title: str
    short_description: str
    llm_responsibilities: list[str]
    llm_skills: list[dict]

    def _get_skills_vector_text(self) -> str:
        skills_names = sorted(set([skill['name'] for skill in self.llm_skills]))
        skills_name_text = " ".join(skills_names)
        return f"short description: {self.short_description.lower()}, skills: {skills_name_text.lower()}"

    def _get_responsibilities_vector_text(self) -> str:
        responsibilities_text = " ".join(sorted(self.llm_responsibilities))
        return f"short description: {self.short_description.lower()}, responsibilities: {responsibilities_text.lower()}"

@dataclass
class IndexableJobDocument(BaseJobDocument):
    job_id: str
    selected_titles: list[str]

    def _get_document_id(self):
        text_content = f"{self.company_slug}-{self._get_skills_vector_text()}-{self._get_responsibilities_vector_text()}"
        return str(uuid.uuid5(uuid.NAMESPACE_URL, text_content))
    
    def _get_payload(self):
        return {
            "job_id": self.job_id,
            "titles": self.selected_titles
        }

@dataclass
class SearchableJobDocument(BaseJobDocument):
    pass

@dataclass
class SearchResult:
    job_id: str
    titles: list[str]
    score: float

    def __init__(self, vector_result: dict):
        self.job_id = vector_result['payload']['job_id']
        self.titles = vector_result['payload']['titles']
        self.score = vector_result['score']