from backend.rag.index import RagIndex
from backend.rag.generator import RagGenerator

def test_rag_search() -> None:
    index = RagIndex()
    index.build_from_directory()
    results = index.search(
        "What separates the cell from the external environment?",
        domain="biology",
    )
    assert results
    assert "cell membrane" in results[0]["text"].lower()

def test_rag_generation() -> None:
    index = RagIndex()
    index.build_from_directory()
    result = RagGenerator(index).generate(
        "The cell membrane contains protein.", domain="biology"
    )
    assert result["document_context"]
    assert result["terminology_context"]
