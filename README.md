# RAG App Starter

## Overview

Starter template for a Retrieval-Augmented Generation (RAG) application using FastAPI, MongoDB for full-text search, Qdrant as a vector database, and Cohere for embeddings.

## Features

* File upload with PDF/Text extraction
* Full-text search with MongoDB text indexes
* Semantic search with Cohere embeddings + Qdrant
* Class-based services/repositories
* Config-driven, no hardcoded values
* Dependency Injection container

## Requirements

* Python 3.10+
* MongoDB (local or remote)
* Qdrant (local or remote)
* Cohere API key

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

## Environment Variables

Create `.env` in project root:

```env
APP_NAME=rag-app
MONGO_URI=mongodb://localhost:27017
MONGO_DB=rag
MONGO_COLLECTION=documents
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=rag_chunks
COHERE_API_KEY=your_api_key
COHERE_EMBED_MODEL=embed-english-v3.0
FILE_CHUNK_SIZE=200
MAX_SEARCH_RESULTS=10
```

## Running the App

```bash
uvicorn app.main:app --reload
```

Open: `http://127.0.0.1:8000`

## API Endpoints

**POST** `/upload-files` – upload PDF/TXT

**GET** `/search/fulltext?q=...` – MongoDB full-text search

**GET** `/search/semantic?q=...` – Cohere + Qdrant semantic search

## License

MIT
