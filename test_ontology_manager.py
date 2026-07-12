from backend.graph.store import KnowledgeGraph
from backend.ontology.manager import OntologyManager


def test_seed_ontology_is_valid() -> None:
    manager = OntologyManager(KnowledgeGraph())
    result = manager.validate()
    assert result["valid"] is True
    assert result["node_count"] >= 7
