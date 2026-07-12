"""Retrieval-guided generation prototype.

This module does not call an external LLM. It retrieves semantically related
terminology, applies exact terminology replacements, and returns a structured
generation context. A later LLM adapter can consume the same context.
"""

from __future__ import annotations

from typing import Any

from backend.semantic.domain_detector import detect_domain
from backend.translator.terminology import apply_terminology
from backend.vector.index import VectorIndex


class RetrievalGenerator:
    def __init__(self, vector_index: VectorIndex | None = None) -> None:
        self.vector_index = vector_index or VectorIndex()

    def generate(
        self,
        text: str,
        source_language: str = "en",
        target_language: str = "ru",
        domain: str = "auto",
        top_k: int = 5,
    ) -> dict[str, Any]:
        if not text.strip():
            raise ValueError("Text must not be empty.")

        resolved_domain = detect_domain(text) if domain == "auto" else domain
        retrieved = self.vector_index.search(
            query=text,
            top_k=top_k,
            domain=resolved_domain,
            minimum_score=0.0,
        )

        translated_text, used_terms = apply_terminology(
            text=text,
            domain=resolved_domain,
            source_language=source_language,
            target_language=target_language,
        )

        context = [
            {
                "semantic_id": item["semantic_id"],
                "source": item["source"],
                "target": item["target"],
                "definition": item["definition"],
                "score": item["score"],
            }
            for item in retrieved
        ]

        return {
            "original_text": text,
            "generated_text": translated_text,
            "source_language": source_language,
            "target_language": target_language,
            "domain": resolved_domain,
            "retrieved_context": context,
            "used_terms": used_terms,
            "generation_mode": "local-retrieval-prototype",
        }
