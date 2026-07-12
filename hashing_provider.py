from backend.embeddings.base import EmbeddingProvider
from backend.vector.vectorizer import HashingVectorizer

class HashingEmbeddingProvider(EmbeddingProvider):
    def __init__(self) -> None:
        self.vectorizer = HashingVectorizer()

    @property
    def dimensions(self) -> int:
        return self.vectorizer.config.dimensions

    def encode(self, text: str) -> list[float]:
        return self.vectorizer.encode(text)
