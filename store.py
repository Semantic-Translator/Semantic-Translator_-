"""Persistent Semantic Knowledge Graph."""

from __future__ import annotations

import json
import re
import uuid
from collections import deque
from dataclasses import asdict
from pathlib import Path
from typing import Any

from backend.embeddings.hashing_provider import HashingEmbeddingProvider
from backend.graph.models import ConceptNode, ConceptRelation
from backend.vector.vectorizer import cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_GRAPH_PATH = PROJECT_ROOT / "storage" / "knowledge_graph" / "graph.json"
TOKEN_RE = re.compile(r"[\w\-]+", flags=re.UNICODE)


class KnowledgeGraph:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DEFAULT_GRAPH_PATH
        self.embedding_provider = HashingEmbeddingProvider()
        self.nodes: dict[str, ConceptNode] = {}
        self.relations: dict[str, ConceptRelation] = {}
        self.load()

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(TOKEN_RE.findall(text.casefold()))

    @staticmethod
    def _node_text(node: ConceptNode) -> str:
        labels = " ".join(node.labels.values())
        aliases = " ".join(
            alias
            for values in node.aliases.values()
            for alias in values
        )
        return " | ".join(
            value for value in [
                node.semantic_id,
                node.domain,
                labels,
                aliases,
                node.definition,
            ] if value
        )

    def add_node(
        self,
        semantic_id: str,
        domain: str,
        labels: dict[str, str],
        aliases: dict[str, list[str]] | None = None,
        definition: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> ConceptNode:
        if not semantic_id.strip():
            raise ValueError("semantic_id must not be empty.")
        if not labels:
            raise ValueError("At least one label is required.")

        node = ConceptNode(
            semantic_id=semantic_id,
            domain=domain,
            labels=labels,
            aliases=aliases or {},
            definition=definition,
            metadata=metadata or {},
        )
        node.vector = self.embedding_provider.encode(self._node_text(node))
        self.nodes[semantic_id] = node
        self.save()
        return node

    def add_relation(
        self,
        source_id: str,
        relation_type: str,
        target_id: str,
        confidence: float = 1.0,
        metadata: dict[str, Any] | None = None,
        relation_id: str | None = None,
    ) -> ConceptRelation:
        if source_id not in self.nodes:
            raise KeyError(f"Unknown source node: {source_id}")
        if target_id not in self.nodes:
            raise KeyError(f"Unknown target node: {target_id}")

        rid = relation_id or str(uuid.uuid4())
        relation = ConceptRelation(
            relation_id=rid,
            source_id=source_id,
            relation_type=relation_type,
            target_id=target_id,
            confidence=confidence,
            metadata=metadata or {},
        )
        self.relations[rid] = relation
        self.save()
        return relation

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "0.6.0",
            "nodes": [asdict(node) for node in self.nodes.values()],
            "relations": [asdict(rel) for rel in self.relations.values()],
        }
        self.path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self) -> None:
        if not self.path.exists():
            self.save()
            return

        data = json.loads(self.path.read_text(encoding="utf-8"))
        self.nodes = {
            item["semantic_id"]: ConceptNode(**item)
            for item in data.get("nodes", [])
        }
        self.relations = {
            item["relation_id"]: ConceptRelation(**item)
            for item in data.get("relations", [])
        }

    def neighbors(
        self,
        semantic_id: str,
        relation_type: str | None = None,
        direction: str = "both",
    ) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []

        for relation in self.relations.values():
            if relation_type and relation.relation_type != relation_type:
                continue

            include = False
            neighbor_id = None
            edge_direction = None

            if direction in {"out", "both"} and relation.source_id == semantic_id:
                include = True
                neighbor_id = relation.target_id
                edge_direction = "out"

            if direction in {"in", "both"} and relation.target_id == semantic_id:
                include = True
                neighbor_id = relation.source_id
                edge_direction = "in"

            if include and neighbor_id in self.nodes:
                node = self.nodes[neighbor_id]
                results.append({
                    "semantic_id": neighbor_id,
                    "labels": node.labels,
                    "domain": node.domain,
                    "relation_type": relation.relation_type,
                    "direction": edge_direction,
                    "confidence": relation.confidence,
                })

        return results

    def shortest_path(
        self,
        source_id: str,
        target_id: str,
        max_depth: int = 6,
    ) -> list[dict[str, Any]]:
        if source_id not in self.nodes or target_id not in self.nodes:
            return []

        queue = deque([(source_id, [])])
        visited = {source_id}

        while queue:
            current, path = queue.popleft()

            if len(path) >= max_depth:
                continue

            for relation in self.relations.values():
                if relation.source_id != current:
                    continue

                step = {
                    "source_id": relation.source_id,
                    "relation_type": relation.relation_type,
                    "target_id": relation.target_id,
                    "confidence": relation.confidence,
                }
                next_path = path + [step]

                if relation.target_id == target_id:
                    return next_path

                if relation.target_id not in visited:
                    visited.add(relation.target_id)
                    queue.append((relation.target_id, next_path))

        return []

    @staticmethod
    def lexical_overlap(query: str, text: str) -> float:
        q = set(TOKEN_RE.findall(query.casefold()))
        t = set(TOKEN_RE.findall(text.casefold()))
        return len(q & t) / len(q) if q else 0.0

    def search(
        self,
        query: str,
        domain: str | None = None,
        top_k: int = 10,
    ) -> list[dict[str, Any]]:
        query_vector = self.embedding_provider.encode(query)
        results: list[dict[str, Any]] = []

        relation_counts: dict[str, int] = {}
        for relation in self.relations.values():
            relation_counts[relation.source_id] = relation_counts.get(relation.source_id, 0) + 1
            relation_counts[relation.target_id] = relation_counts.get(relation.target_id, 0) + 1

        max_relations = max(relation_counts.values(), default=1)

        for node in self.nodes.values():
            if domain and domain != "auto" and node.domain != domain:
                continue

            node_text = self._node_text(node)
            vector_score = max(cosine_similarity(query_vector, node.vector), 0.0)
            lexical_score = self.lexical_overlap(query, node_text)
            relation_score = relation_counts.get(node.semantic_id, 0) / max_relations

            score = (
                0.60 * vector_score
                + 0.25 * lexical_score
                + 0.15 * relation_score
            )

            results.append({
                "score": round(score, 6),
                "vector_score": round(vector_score, 6),
                "lexical_score": round(lexical_score, 6),
                "relation_score": round(relation_score, 6),
                "semantic_id": node.semantic_id,
                "domain": node.domain,
                "labels": node.labels,
                "aliases": node.aliases,
                "definition": node.definition,
                "relation_count": relation_counts.get(node.semantic_id, 0),
            })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:max(1, top_k)]

    def status(self) -> dict[str, Any]:
        domains = sorted({node.domain for node in self.nodes.values()})
        return {
            "path": str(self.path),
            "exists": self.path.exists(),
            "nodes": len(self.nodes),
            "relations": len(self.relations),
            "domains": domains,
            "dimensions": self.embedding_provider.dimensions,
        }

    def export(self) -> dict[str, Any]:
        return {
            "version": "0.6.0",
            "nodes": [asdict(node) for node in self.nodes.values()],
            "relations": [asdict(rel) for rel in self.relations.values()],
        }
