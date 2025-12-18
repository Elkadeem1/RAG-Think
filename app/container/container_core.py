from app.core.config import get_settings
from app.clients.nosql_client import MongoClientFactory
from app.clients.vetordb_client import QdrantClientFactory
from app.clients.embedding_client import CohereClient
from app.repositories.mongo_repository import MongoRepository
from app.repositories.qdrant_repository import QdrantRepository
from app.services.file_service import FileService
from app.services.fulltext_services import FullTextService
from app.services.semantic_services import SemanticService

class Container:
    def __init__(self):
        settings = get_settings()
        self.mongo = MongoClientFactory(settings)
        self.qdrant = QdrantClientFactory(settings)
        self.cohere = CohereClient(settings)
        self.mongo_repo = MongoRepository(self.mongo, settings)
        self.qdrant_repo = QdrantRepository(self.qdrant, settings)
        self.file_service = FileService(self.mongo_repo, self.qdrant_repo, self.cohere, settings)
        self.fulltext_service = FullTextService(self.mongo_repo, settings)
        self.semantic_service = SemanticService(self.qdrant_repo, self.cohere, settings)

    async def startup(self):
        await self.mongo_repo.ensure_indexes()
        await self.qdrant_repo.ensure_collection()

container = Container()