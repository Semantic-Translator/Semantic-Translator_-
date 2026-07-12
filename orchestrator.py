"""Full LLM-oriented translation orchestration."""

from __future__ import annotations

from typing import Any

from backend.generation.advanced_translator import AdvancedTranslator
from backend.llm.logger import log_generation
from backend.llm.router import ProviderRouter
from backend.prompts.builder import build_translation_prompt


PROFILES = {
    "scientific": {"temperature": 0.1, "max_tokens": 1200},
    "literal": {"temperature": 0.0, "max_tokens": 1000},
    "explanatory": {"temperature": 0.3, "max_tokens": 1800},
}


class LLMTranslationOrchestrator:
    def __init__(
        self,
        advanced_translator: AdvancedTranslator | None = None,
    ) -> None:
        self.advanced_translator = advanced_translator or AdvancedTranslator()

    def translate(
        self,
        *,
        text: str,
        source_language: str = "en",
        target_language: str = "ru",
        domain: str = "auto",
        profile: str = "scientific",
        provider: str = "local",
        top_k: int = 5,
        reuse_threshold: float = 0.85,
    ) -> dict[str, Any]:
        base = self.advanced_translator.translate(
            text=text,
            source_language=source_language,
            target_language=target_language,
            domain=domain,
            top_k=top_k,
            reuse_threshold=reuse_threshold,
        )

        prompt = build_translation_prompt(
            source_text=text,
            source_language=source_language,
            target_language=target_language,
            domain=base["domain"],
            profile=profile,
            terminology_context=base["terminology_context"],
            memory_matches=base["memory_matches"],
            document_context=base["document_context"],
            deterministic_candidate=base["translated_text"],
        )

        settings = PROFILES.get(profile, PROFILES["scientific"])
        router = ProviderRouter.from_name(provider)
        result = router.generate(
            prompt,
            temperature=settings["temperature"],
            max_tokens=settings["max_tokens"],
        )

        log_id = log_generation(
            provider=result.provider,
            model=result.model,
            prompt=prompt,
            output=result.text,
            metadata=result.metadata,
        )

        return {
            **base,
            "translated_text": result.text,
            "llm_provider": result.provider,
            "llm_model": result.model,
            "llm_metadata": result.metadata,
            "profile": profile,
            "log_id": log_id,
            "generation_mode": "llm-orchestrated-translation",
        }

    def health(self, provider: str = "local") -> dict[str, Any]:
        return ProviderRouter.from_name(provider).health()
