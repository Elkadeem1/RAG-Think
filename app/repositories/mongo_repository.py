from typing import List, Dict, Any
from app.clients.nosql_client import MongoClientFactory
from app.core.config import Settings
from bson import ObjectId

class MongoRepository:
    def __init__(self, mongo: MongoClientFactory, settings: Settings):
        self._db = mongo.db
        self._collection_name = settings.MONGO_COLLECTION
        self._max_results = settings.MAX_SEARCH_RESULTS

    @property
    def collection(self):
        return self._db[self._collection_name]

    async def ensure_indexes(self):
        await self.collection.create_index([("content", "text")])

    async def insert_document(self, doc: Dict[str, Any]) -> str:
        res = await self.collection.insert_one(doc)
        return str(res.inserted_id)

    async def insert_many(self, docs: List[Dict[str, Any]]):
        await self.collection.insert_many(docs)

    async def full_text_search(self, query: str) -> List[Dict[str, Any]]:
        cursor = self.collection.find({"$text": {"$search": query}}).limit(self._max_results)
        results = []
        async for d in cursor:
            d["_id"] = str(d["_id"]) if isinstance(d.get("_id"), ObjectId) else d.get("_id")
            results.append(d)
        return results