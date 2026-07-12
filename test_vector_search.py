from backend.vector.index import VectorIndex
from backend.vector.vectorizer import HashingVectorizer, cosine_similarity


def test_vector_dimensions() -> None:
    vector = HashingVectorizer().encode("cell membrane")
    assert len(vector) == 384


def test_identical_similarity() -> None:
    vectorizer = HashingVectorizer()
    left = vectorizer.encode("cell membrane")
    right = vectorizer.encode("cell membrane")
    assert cosine_similarity(left, right) > 0.99


def test_vector_index_search() -> None:
    index = VectorIndex()
    index.build()
    results = index.search("biological cell membrane", top_k=3, domain="biology")
    assert results
    assert any(item["semantic_id"] == "BIO-000002" for item in results)
