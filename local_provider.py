"""Deterministic local fallback provider."""

from __future__ import annotations

from backend.llm.base import GenerationResult, LLMProvider


class LocalDeterministicProvider(LLMProvider):
    name = "local"

    def __init__(self, model: str = "semantic-local-v0") -> None:
        self.model = model

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        max_tokens: int = 1200,
    ) -> GenerationResult:
        marker = "FINAL_TRANSLATION:"
        if marker in prompt:
            candidate = prompt.split(marker, 1)[1].strip()
        else:
            candidate = prompt.strip()

        text = candidate[:max_tokens * 4].strip()

        return GenerationResult(
            text=text,
            provider=self.name,
            model=self.model,
            metadata={
                "mode": "deterministic-local-fallback",
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
        )

    def health(self) -> dict:
        return {
            "provider": self.name,
            "model": self.model,
            "available": True,
            "mode": "offline",
        }
