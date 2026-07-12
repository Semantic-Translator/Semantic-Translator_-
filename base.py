"""LLM provider abstraction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class GenerationResult:
    text: str
    provider: str
    model: str
    metadata: dict[str, Any]


class LLMProvider(ABC):
    name: str = "unknown"

    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        max_tokens: int = 1200,
    ) -> GenerationResult:
        raise NotImplementedError

    @abstractmethod
    def health(self) -> dict[str, Any]:
        raise NotImplementedError
