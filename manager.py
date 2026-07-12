"""Ontology import and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from backend.graph.store import KnowledgeGraph


ALLOWED_RELATIONS = {
    "is-a",
    "part-of",
    "has-part",
    "related-to",
    "causes",
    "regulates",
    "located-in",
    "expressed-in",
    "derived-from",
}


class OntologyManager:
    def __init__(self, graph: KnowledgeGraph | None = None) -> None:
        self.graph = graph or KnowledgeGraph()

    def import_json(self, path: Path) -> dict[str, int]:
        data = json.loads(path.read_text(encoding="utf-8"))

        node_count = 0
        relation_count = 0

        for node in data.get("nodes", []):
            self.graph.add_node(
                semantic_id=node["semantic_id"],
                domain=node.get("domain", "common"),
                labels=node.get("labels", {}),
                aliases=node.get("aliases", {}),
                definition=node.get("definition", ""),
                metadata=node.get("metadata", {}),
            )
            node_count += 1

        for relation in data.get("relations", []):
            self.graph.add_relation(
                source_id=relation["source_id"],
                relation_type=relation["relation_type"],
                target_id=relation["target_id"],
                confidence=float(relation.get("confidence", 1.0)),
                metadata=relation.get("metadata", {}),
                relation_id=relation.get("relation_id"),
            )
            relation_count += 1

        return {"nodes": node_count, "relations": relation_count}

    def validate(self) -> dict[str, Any]:
        errors: list[str] = []
        warnings: list[str] = []

        for semantic_id, node in self.graph.nodes.items():
            if not semantic_id:
                errors.append("Node with empty Semantic-ID.")
            if not node.labels:
                errors.append(f"{semantic_id}: no labels.")
            if not node.definition:
                warnings.append(f"{semantic_id}: no definition.")

        for relation in self.graph.relations.values():
            if relation.source_id not in self.graph.nodes:
                errors.append(f"{relation.relation_id}: unknown source.")
            if relation.target_id not in self.graph.nodes:
                errors.append(f"{relation.relation_id}: unknown target.")
            if relation.relation_type not in ALLOWED_RELATIONS:
                warnings.append(
                    f"{relation.relation_id}: non-standard relation "
                    f"{relation.relation_type}."
                )
            if not 0.0 <= relation.confidence <= 1.0:
                errors.append(
                    f"{relation.relation_id}: confidence outside 0..1."
                )

        return {
            "valid": not errors,
            "errors": errors,
            "warnings": warnings,
            "node_count": len(self.graph.nodes),
            "relation_count": len(self.graph.relations),
        }
