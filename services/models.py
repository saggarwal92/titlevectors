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
    hop_level: int
    source: str

    def _get_document_id(self):
        text_content = f"{self.company_slug}-{self._get_skills_vector_text()}-{self._get_responsibilities_vector_text()}"
        return str(uuid.uuid5(uuid.NAMESPACE_URL, text_content))
    
    def _get_payload(self):
        return {
            "job_id": self.job_id,
            "titles": self.selected_titles,
            "hop_level": self.hop_level,
            "source": self.source
        }

@dataclass
class SearchableJobDocument(BaseJobDocument):
    pass


@dataclass
class SearchResult:
    job_id: str
    titles: list[str]
    score: float
    hop_level: int
    source: str

    def __init__(self, vector_result: dict):
        self.job_id = vector_result['payload']['job_id']
        self.titles = vector_result['payload']['titles']
        self.score = vector_result['score']
        self.hop_level = vector_result['payload']['hop_level']
        self.source = vector_result['payload']['source']
    
    def _adjusted_score(self) -> float:
        MIN_LEVEL = 0.6
        LEVEL_PENALTY = 0.12
        SOURCE_FACTORS = {
            "human": 1.1,
            "taxonomy": 1.1, # when taxonomy matches for both the llm titles
            "gpt_verified": 1.0,  # when vector or taxonomy result is gpt verified
            "vector_auto": 0.95,
            "gpt_suggest": 0.95,
        }
        level_factor = max(MIN_LEVEL, 1.0 - (self.hop_level * LEVEL_PENALTY))
        source_factor = SOURCE_FACTORS.get(self.source, 0.8)
        return min(self.score * level_factor * source_factor, self.score)
