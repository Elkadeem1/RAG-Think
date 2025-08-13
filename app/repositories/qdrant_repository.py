from typing import List, Dict, Any
from app.clients.vetordb_client import QdrantClientFactory
from app.core.config import Settings
from qdrant_client.http.models import VectorParams, Distance, PointStruct

class QdrantRepository:
    def __init__(self, qdrant: QdrantClientFactory, settings: Settings):
        self._client = qdrant.client
        self._collection = settings.QDRANT_COLLECTION
        self._limit = settings.MAX_SEARCH_RESULTS

    async def ensure_collection(self):
        exists = self._client.get_collection(self._collection) if self._collection in [c.name for c in self._client.get_collections().collections] else None
        if not exists:
            self._client.recreate_collection(collection_name=self._collection, vectors_config=VectorParams(size=1024, distance=Distance.COSINE))

    def upsert_vectors(self, points: List[PointStruct]):
        self._client.upsert(collection_name=self._collection, points=points)

    def search(self, vector: List[float]) -> List[Dict[str, Any]]:
        r = self._client.search(collection_name=self._collection, query_vector=vector, limit=self._limit)
        return [dict(id=x.id, score=x.score, payload=x.payload) for x in r]