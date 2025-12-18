import io
import uuid
import pdfplumber
from typing import List, Dict
from app.repositories.mongo_repository import MongoRepository
from app.repositories.qdrant_repository import QdrantRepository
from app.clients.embedding_client import CohereClient
from app.core.config import Settings
from qdrant_client.http.models import PointStruct

class FileService:
    def __init__(self, mongo_repo: MongoRepository, qdrant_repo: QdrantRepository, cohere: CohereClient, settings: Settings):
        self.mongo_repo = mongo_repo
        self.qdrant_repo = qdrant_repo
        self.cohere = cohere
        self.chunk_size = settings.FILE_CHUNK_SIZE

    async def upload(self, filename: str, data: bytes) -> Dict[str, str]:
        doc_id = str(uuid.uuid4())
        text = self._extract_text(filename, data)
        chunks = self._chunk(text)
        await self._store_fulltext(doc_id, filename, chunks)
        await self._store_vectors(doc_id, chunks)
        return {"document_id": doc_id, "chunks": str(len(chunks))}

    def _extract_text(self, filename: str, data: bytes) -> str:
        if filename.lower().endswith(".pdf"):
            with pdfplumber.open(io.BytesIO(data)) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
                return "\n".join(pages)
        return data.decode("utf-8", errors="ignore")

    def _chunk(self, text: str) -> List[str]:
        words = text.split()
        chunks, buf = [], []
        for w in words:
            buf.append(w)
            if len(buf) >= self.chunk_size:
                chunks.append(" ".join(buf))
                buf = []
        if buf:
            chunks.append(" ".join(buf))
        return chunks

    async def _store_fulltext(self, doc_id: str, filename: str, chunks: List[str]):
        docs = [{"document_id": doc_id, "filename": filename, "chunk_id": i, "content": c} for i, c in enumerate(chunks)]
        await self.mongo_repo.insert_many(docs)

    async def _store_vectors(self, doc_id: str, chunks: List[str]):
        vectors = self.cohere.embed(chunks)
        points = [PointStruct(id=str(uuid.uuid4()), vector=v, payload={"document_id": doc_id, "chunk_id": i, "text": t}) for i, (v, t) in enumerate(zip(vectors, chunks))]
        self.qdrant_repo.upsert_vectors(points)