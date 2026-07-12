from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

from backend.semantic.domain_detector import detect_domain
from backend.translator.engine import TranslationEngine
from backend.translator.terminology import search_terms


app = FastAPI(
    title="Semantic-Translator API",
    version="0.1.1",
    description="Semantic translation platform API",
)

engine = TranslationEngine()


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


@app.get("/")
def root() -> dict:
    return {
        "project": "Semantic-Translator",
        "version": "0.1.1",
        "status": "ready",
    }


@app.get("/domains/detect")
def detect_text_domain(text: str = Query(min_length=1)) -> dict:
    return {
        "text": text,
        "domain": detect_domain(text),
    }


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
    return {
        "query": query,
        "domain": domain,
        "count": len(terms),
        "terms": terms,
    }


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
