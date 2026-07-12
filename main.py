from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="Semantic-Translator API",
    version="0.1.0",
    description="Semantic translation platform API",
)


class TranslationRequest(BaseModel):
    text: str
    source_language: str = "auto"
    target_language: str = "ru"
    domain: str = "common"


class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    domain: str
    status: str


@app.get("/")
def root() -> dict:
    return {
        "project": "Semantic-Translator",
        "version": "0.1.0",
        "status": "ready",
    }


@app.post("/translate", response_model=TranslationResponse)
def translate(payload: TranslationRequest) -> TranslationResponse:
    return TranslationResponse(
        original_text=payload.text,
        translated_text=payload.text,
        source_language=payload.source_language,
        target_language=payload.target_language,
        domain=payload.domain,
        status="prototype",
    )
