"""Deterministic local vectorizer.

The implementation intentionally avoids large external dependencies. It creates
a fixed-size vector from word and character n-grams using stable hashing.
"""

from __future__ import annotations

import hashlib
import math
import re
from dataclasses import dataclass


_TOKEN_RE = re.compile(r"[\w\-]+", flags=re.UNICODE)


@dataclass(frozen=True)
class VectorizerConfig:
    dimensions: int = 384
    word_ngram_min: int = 1
    word_ngram_max: int = 2
    character_ngram_min: int = 3
    character_ngram_max: int = 5


class HashingVectorizer:
    def __init__(self, config: VectorizerConfig | None = None) -> None:
        self.config = config or VectorizerConfig()

        if self.config.dimensions <= 0:
            raise ValueError("Vector dimensions must be positive.")

    @staticmethod
    def normalize_text(text: str) -> str:
        return " ".join(_TOKEN_RE.findall(text.casefold()))

    @staticmethod
    def _stable_hash(value: str) -> int:
        digest = hashlib.blake2b(value.encode("utf-8"), digest_size=8).digest()
        return int.from_bytes(digest, byteorder="big", signed=False)

    def _features(self, text: str) -> list[str]:
        normalized = self.normalize_text(text)
        words = normalized.split()
        features: list[str] = []

        for size in range(self.config.word_ngram_min, self.config.word_ngram_max + 1):
            for index in range(len(words) - size + 1):
                features.append("w:" + " ".join(words[index:index + size]))

        compact = normalized.replace(" ", "_")
        for size in range(
            self.config.character_ngram_min,
            self.config.character_ngram_max + 1,
        ):
            for index in range(len(compact) - size + 1):
                features.append("c:" + compact[index:index + size])

        return features

    def encode(self, text: str) -> list[float]:
        vector = [0.0] * self.config.dimensions

        for feature in self._features(text):
            hash_value = self._stable_hash(feature)
            position = hash_value % self.config.dimensions
            sign = 1.0 if ((hash_value >> 1) & 1) == 0 else -1.0
            vector[position] += sign

        norm = math.sqrt(sum(value * value for value in vector))
        if norm:
            vector = [value / norm for value in vector]

        return vector


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("Vectors must have equal dimensions.")

    return sum(a * b for a, b in zip(left, right))
