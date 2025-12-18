from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import Settings

class MongoClientFactory:
    def __init__(self, settings: Settings):
        self._client = AsyncIOMotorClient(settings.MONGO_URI)
        self._db = self._client[settings.MONGO_DB]

    @property
    def db(self):
        return self._db