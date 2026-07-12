from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from backend.generation.retrieval_generator import RetrievalGenerator
from backend.semantic.domain_detector import detect_domain
from backend.translator.engine import TranslationEngine
from backend.translator.terminology import search_terms
from backend.vector.index import VectorIndex


app = FastAPI(
    title="Semantic-Translator API",
    version="0.2.0",
    description="Semantic translation platform with vector-oriented retrieval",
)

engine = TranslationEngine()
vector_index = VectorIndex()
generator = RetrievalGenerator(vector_index)


class TranslationRequest(BaseModel):
    text: str = Field(min_length=1)
    source_language: str = "en"
    target_language: str = "ru"
    domain: str = "auto"


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    domain: str
    used_terms: list[dict]
    status: str


class VectorSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=50)
    domain: str = "auto"
    minimum_score: float = Field(default=0.0, ge=-1.0, le=1.0)


class GenerationRequest(BaseModel):
    text: str = Field(min_length=1)
    source_language: str = "en"
    target_language: str = "ru"
    domain: str = "auto"
    top_k: int = Field(default=5, ge=1, le=50)


@app.get("/")
def root() -> dict:
    return {
        "project": "Semantic-Translator",
        "version": "0.2.0",
        "status": "ready",
        "vector_search": True,
    }


@app.get("/domains/detect")
def detect_text_domain(text: str = Query(min_length=1)) -> dict:
    return {"text": text, "domain": detect_domain(text)}


@app.get("/terms/search")
def find_terms(
    query: str = "",
    domain: str = "biology",
    source_language: str = "en",
    target_language: str = "ru",
) -> dict:
    terms = search_terms(
        query=query,
        domain=domain,
        source_language=source_language,
        target_language=target_language,
    )
    return {"query": query, "domain": domain, "count": len(terms), "terms": terms}


@app.post("/translate", response_model=TranslationResponse)
def translate(payload: TranslationRequest) -> TranslationResponse:
    domain = detect_domain(payload.text) if payload.domain == "auto" else payload.domain
    translated_text, used_terms = engine.translate(
        text=payload.text,
        source_language=payload.source_language,
        target_language=payload.target_language,
        domain=domain,
    )
    return TranslationResponse(
        original_text=payload.text,
        translated_text=translated_text,
        source_language=payload.source_language,
        target_language=payload.target_language,
        domain=domain,
        used_terms=used_terms,
        status="terminology-prototype",
    )


@app.post("/vectors/rebuild")
def rebuild_vectors() -> dict:
    count = vector_index.build()
    return {"status": "rebuilt", "records": count}


@app.get("/vectors/status")
def vector_status() -> dict:
    return vector_index.status()


@app.post("/vectors/search")
def vector_search(payload: VectorSearchRequest) -> dict:
    domain = None if payload.domain == "auto" else payload.domain
    results = vector_index.search(
        query=payload.query,
        top_k=payload.top_k,
        domain=domain,
        minimum_score=payload.minimum_score,
    )
    return {"query": payload.query, "count": len(results), "results": results}


@app.post("/generate")
def generate(payload: GenerationRequest) -> dict:
    return generator.generate(
        text=payload.text,
        source_language=payload.source_language,
        target_language=payload.target_language,
        domain=payload.domain,
        top_k=payload.top_k,
    )
