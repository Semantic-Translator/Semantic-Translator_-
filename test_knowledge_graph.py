from pathlib import Path
from tempfile import TemporaryDirectory

from backend.graph.store import KnowledgeGraph


def test_add_and_search_graph() -> None:
    with TemporaryDirectory() as tmp:
        graph = KnowledgeGraph(Path(tmp) / "graph.json")
        graph.add_node(
            "BIO-1",
            "biology",
            {"en": "cell", "ru": "клетка"},
            definition="Basic unit of life.",
        )
        graph.add_node(
            "BIO-2",
            "biology",
            {"en": "cell membrane", "ru": "клеточная мембрана"},
            definition="Boundary of the cell.",
        )
        graph.add_relation("BIO-2", "part-of", "BIO-1")

        results = graph.search("cell membrane", domain="biology")
        assert results
        assert results[0]["semantic_id"] == "BIO-2"

        neighbors = graph.neighbors("BIO-2")
        assert neighbors
        assert neighbors[0]["semantic_id"] == "BIO-1"
