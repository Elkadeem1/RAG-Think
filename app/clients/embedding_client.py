import cohere
from app.core.config import Settings

class CohereClient:
    def __init__(self, settings: Settings):
        self._client = cohere.Client(api_key=settings.COHERE_API_KEY)
        self._model = settings.COHERE_EMBED_MODEL

    def embed(self, texts: list[str]) -> list[list[float]]:
        resp = self._client.embed(texts=texts, model=self._model)
        return resp.embeddings