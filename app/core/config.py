from pydantic import BaseSettings, Field
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = Field(default="rag-app")
    MONGO_URI: str
    MONGO_DB: str
    MONGO_COLLECTION: str
    QDRANT_HOST: str
    QDRANT_PORT: int
    QDRANT_COLLECTION: str
    COHERE_API_KEY: str
    COHERE_EMBED_MODEL: str
    FILE_CHUNK_SIZE: int = 800
    MAX_SEARCH_RESULTS: int = 10
    class Config:
        env_file = ".env"

@lru_cache
def get_settings() -> Settings:
    return Settings()