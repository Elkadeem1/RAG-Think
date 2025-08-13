from qdrant_client import QdrantClient
from app.core.config import Settings

class QdrantClientFactory:
    def __init__(self, settings: Settings):
        self._client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

    @property
    def client(self) -> QdrantClient:
        return self._client