from typing import List, Dict
from app.repositories.mongo_repository import MongoRepository
from app.core.config import Settings

class FullTextService:
    def __init__(self, mongo_repo: MongoRepository, settings: Settings):
        self.mongo_repo = mongo_repo
        self.limit = settings.MAX_SEARCH_RESULTS

    async def search(self, query: str) -> List[Dict]:
        return await self.mongo_repo.full_text_search(query)