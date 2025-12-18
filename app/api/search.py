from fastapi import APIRouter, HTTPException, Query
from app.container.container_core import container

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/fulltext")
async def full_text_search(q: str = Query(..., min_length=1)):
    try:
        return await container.fulltext_service.search(q)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/semantic")
async def semantic_search(q: str = Query(..., min_length=1)):
    try:
        return container.semantic_service.search(q)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))