"""Advanced local translator with memory + RAG + terminology fusion."""

from __future__ import annotations

from typing import Any

from backend.memory.index import TranslationMemory
from backend.quality.scorer import score_translation
from backend.rag.generator import RagGenerator
from backend.semantic.domain_detector import detect_domain


class AdvancedTranslator:
    def __init__(
        self,
        translation_memory: TranslationMemory | None = None,
        rag_generator: RagGenerator | None = None,
    ) -> None:
        self.translation_memory = translation_memory or TranslationMemory()
        self.rag_generator = rag_generator or RagGenerator()

    def translate(
        self,
        text: str,
        source_language: str = "en",
        target_language: str = "ru",
        domain: str = "auto",
        top_k: int = 5,
        reuse_threshold: float = 0.85,
    ) -> dict[str, Any]:
        resolved_domain = detect_domain(text) if domain == "auto" else domain

        memory_matches = self.translation_memory.search(
            query=text,
            source_language=source_language,
            target_language=target_language,
            domain=resolved_domain,
            top_k=top_k,
            approved_only=True,
            minimum_score=0.0,
        )

        reused = False
        reused_memory_id = None

        if memory_matches and memory_matches[0]["score"] >= reuse_threshold:
            generated_text = memory_matches[0]["target_text"]
            reused = True
            reused_memory_id = memory_matches[0]["memory_id"]
            rag_result = self.rag_generator.generate(
                text=text,
                source_language=source_language,
                target_language=target_language,
                domain=resolved_domain,
                top_k=top_k,
            )
        else:
            rag_result = self.rag_generator.generate(
                text=text,
                source_language=source_language,
                target_language=target_language,
                domain=resolved_domain,
                top_k=top_k,
            )
            generated_text = rag_result["generated_text"]

        quality = score_translation(
            used_terms=rag_result["used_terms"],
            memory_matches=memory_matches,
            document_context=rag_result["document_context"],
        )

        return {
            "original_text": text,
            "translated_text": generated_text,
            "source_language": source_language,
            "target_language": target_language,
            "domain": resolved_domain,
            "memory_matches": memory_matches,
            "memory_reused": reused,
            "reused_memory_id": reused_memory_id,
            "document_context": rag_result["document_context"],
            "terminology_context": rag_result["terminology_context"],
            "used_terms": rag_result["used_terms"],
            "quality": quality,
            "generation_mode": (
                "approved-translation-memory"
                if reused
                else "hybrid-rag-memory-prototype"
            ),
        }
