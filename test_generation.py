from backend.generation.retrieval_generator import RetrievalGenerator
from backend.vector.index import VectorIndex


def test_retrieval_generation() -> None:
    index = VectorIndex()
    index.build()
    generator = RetrievalGenerator(index)
    result = generator.generate(
        "The cell membrane contains protein and DNA.",
        domain="biology",
    )
    assert result["domain"] == "biology"
    assert result["retrieved_context"]
    assert "клеточная мембрана" in result["generated_text"]
