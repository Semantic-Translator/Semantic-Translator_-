from fastapi import FastAPI
from pydantic import BaseModel, Field

from backend.llm.orchestrator import LLMTranslationOrchestrator


app = FastAPI(
    title="Semantic-Translator API",
    version="0.5.0",
    description="Semantic translator with vector memory, RAG and LLM orchestration",
)

orchestrator = LLMTranslationOrchestrator()


class LLMTranslationRequest(BaseModel):
    text: str = Field(min_length=1)
    source_language: str = "en"
    target_language: str = "ru"
    domain: str = "auto"
    profile: str = "scientific"
    provider: str = "local"
    top_k: int = Field(default=5, ge=1, le=50)
    reuse_threshold: float = Field(default=0.85, ge=0.0, le=1.0)


@app.get("/")
def root() -> dict:
    return {
        "project": "Semantic-Translator",
        "version": "0.5.0",
        "vector_search": True,
        "rag": True,
        "translation_memory": True,
        "llm_orchestration": True,
    }


@app.get("/llm/health")
def llm_health(provider: str = "local") -> dict:
    return orchestrator.health(provider)


@app.post("/translate/llm")
def translate_llm(payload: LLMTranslationRequest) -> dict:
    return orchestrator.translate(
        text=payload.text,
        source_language=payload.source_language,
        target_language=payload.target_language,
        domain=payload.domain,
        profile=payload.profile,
        provider=payload.provider,
        top_k=payload.top_k,
        reuse_threshold=payload.reuse_threshold,
    )
