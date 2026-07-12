from backend.embeddings.base import EmbeddingProvider

class SentenceTransformersProvider(EmbeddingProvider):
    def __init__(self, model_name: str) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as error:
            raise RuntimeError("Install sentence-transformers first.") from error
        self.model = SentenceTransformer(model_name)
        self._dimensions = int(self.model.get_sentence_embedding_dimension())

    @property
    def dimensions(self) -> int:
        return self._dimensions

    def encode(self, text: str) -> list[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return [float(value) for value in vector]
