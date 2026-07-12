from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.rag.chunker import ChunkingConfig
from backend.rag.generator import RagGenerator
from backend.rag.index import RagIndex
from backend.vector.index import VectorIndex

app = FastAPI(title="Semantic-Translator API", version="0.3.0")
vector_index = VectorIndex()
rag_index = RagIndex()
rag_generator = RagGenerator(rag_index)

class RagIngestRequest(BaseModel):
    path: str
    domain: str | None = None
    chunk_size: int = Field(default=700, ge=100)
    chunk_overlap: int = Field(default=120, ge=0)

class SearchRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=50)
    domain: str = "auto"
    minimum_score: float = Field(default=0.0, ge=0.0, le=1.0)

class GenerateRequest(BaseModel):
    text: str
    source_language: str = "en"
    target_language: str = "ru"
    domain: str = "auto"
    top_k: int = Field(default=5, ge=1, le=50)

@app.get("/")
def root() -> dict:
    return {"project": "Semantic-Translator", "version": "0.3.0",
            "vector_search": True, "rag": True}

@app.post("/vectors/rebuild")
def rebuild_vectors() -> dict:
    return {"status": "rebuilt", "records": vector_index.build()}

@app.get("/rag/status")
def rag_status() -> dict:
    return rag_index.status()

@app.post("/rag/rebuild")
def rag_rebuild() -> dict:
    return {"status": "rebuilt", "chunks": rag_index.build_from_directory()}

@app.post("/rag/ingest")
def rag_ingest(payload: RagIngestRequest) -> dict:
    count = rag_index.ingest_file(
        Path(payload.path),
        payload.domain,
        ChunkingConfig(payload.chunk_size, payload.chunk_overlap),
    )
    return {"status": "ingested", "chunks": count}

@app.post("/rag/search")
def rag_search(payload: SearchRequest) -> dict:
    domain = None if payload.domain == "auto" else payload.domain
    results = rag_index.search(
        payload.query, payload.top_k, domain, payload.minimum_score
    )
    return {"query": payload.query, "count": len(results), "results": results}

@app.post("/rag/generate")
def rag_generate(payload: GenerateRequest) -> dict:
    return rag_generator.generate(
        payload.text, payload.source_language, payload.target_language,
        payload.domain, payload.top_k
    )
