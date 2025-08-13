from typing import List, Dict
from app.repositories.qdrant_repository import QdrantRepository
from app.clients.embedding_client import CohereClient
from app.core.config import Settings

class SemanticService:
    def __init__(self, qdrant_repo: QdrantRepository, cohere: CohereClient, settings: Settings):
        self.qdrant_repo = qdrant_repo
        self.cohere = cohere
        self.limit = settings.MAX_SEARCH_RESULTS

    def search(self, query: str) -> List[Dict]:
        vec = self.cohere.embed([query])[0]
        return self.qdrant_repo.search(vec)