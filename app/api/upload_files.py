from fastapi import APIRouter, UploadFile, File, HTTPException
from app.container.container_core import container

router = APIRouter(prefix="/upload-files", tags=["upload"])

@router.post("")
async def upload_files(file: UploadFile = File(...)):
    data = await file.read()
    try:
        result = await container.file_service.upload(file.filename, data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))