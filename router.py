"""Provider routing and fallback."""

from __future__ import annotations

from backend.llm.base import GenerationResult, LLMProvider
from backend.llm.http_provider import HttpLLMProvider
from backend.llm.local_provider import LocalDeterministicProvider


class ProviderRouter:
    def __init__(
        self,
        primary: LLMProvider | None = None,
        fallback: LLMProvider | None = None,
    ) -> None:
        self.primary = primary or LocalDeterministicProvider()
        self.fallback = fallback or LocalDeterministicProvider()

    @classmethod
    def from_name(cls, provider_name: str) -> "ProviderRouter":
        name = provider_name.casefold()

        if name == "http":
            return cls(
                primary=HttpLLMProvider(),
                fallback=LocalDeterministicProvider(),
            )

        return cls(
            primary=LocalDeterministicProvider(),
            fallback=LocalDeterministicProvider(),
        )

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        max_tokens: int = 1200,
    ) -> GenerationResult:
        try:
            return self.primary.generate(
                prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        except Exception as error:
            result = self.fallback.generate(
                prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            result.metadata["fallback_reason"] = str(error)
            result.metadata["fallback_used"] = True
            return result

    def health(self) -> dict:
        return {
            "primary": self.primary.health(),
            "fallback": self.fallback.health(),
        }
