from abc import ABC, abstractmethod

class EmbeddingProvider(ABC):
    @property
    @abstractmethod
    def dimensions(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def encode(self, text: str) -> list[float]:
        raise NotImplementedError
