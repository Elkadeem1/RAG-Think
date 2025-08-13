import uvicorn
from fastapi import FastAPI
from app.api import upload_files, search
from app.container.container_core import container

app = FastAPI(title=container.__class__.__name__)

app.include_router(upload_files.router)
app.include_router(search.router)

@app.on_event("startup")
async def startup_event():
    await container.startup()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)