from backend.generation.retrieval_generator import RetrievalGenerator
from backend.rag.index import RagIndex
from backend.semantic.domain_detector import detect_domain
from backend.vector.index import VectorIndex

class RagGenerator:
    def __init__(self, rag_index: RagIndex | None = None) -> None:
        self.rag_index = rag_index or RagIndex()
        self.term_generator = RetrievalGenerator(VectorIndex())

    def generate(self, text: str, source_language: str = "en",
                 target_language: str = "ru", domain: str = "auto",
                 top_k: int = 5) -> dict:
        resolved_domain = detect_domain(text) if domain == "auto" else domain
        docs = self.rag_index.search(text, top_k, resolved_domain)
        terms = self.term_generator.generate(
            text, source_language, target_language, resolved_domain, top_k
        )
        return {
            "original_text": text,
            "generated_text": terms["generated_text"],
            "source_language": source_language,
            "target_language": target_language,
            "domain": resolved_domain,
            "document_context": docs,
            "terminology_context": terms["retrieved_context"],
            "used_terms": terms["used_terms"],
            "assembled_context": "\n\n".join(
                f"[{x['title']}#{x['chunk_number']}] {x['text']}" for x in docs
            ),
            "generation_mode": "hybrid-rag-local-prototype",
        }
