"""Graph context for translation and generation."""

from __future__ import annotations

from typing import Any

from backend.graph.store import KnowledgeGraph


class GraphContextBuilder:
    def __init__(self, graph: KnowledgeGraph | None = None) -> None:
        self.graph = graph or KnowledgeGraph()

    def build(
        self,
        query: str,
        domain: str | None = None,
        top_k: int = 5,
        neighbor_limit: int = 5,
    ) -> dict[str, Any]:
        concepts = self.graph.search(query, domain=domain, top_k=top_k)

        enriched = []
        for concept in concepts:
            neighbors = self.graph.neighbors(
                concept["semantic_id"],
                direction="both",
            )[:neighbor_limit]

            enriched.append({
                **concept,
                "neighbors": neighbors,
            })

        return {
            "query": query,
            "domain": domain,
            "concepts": enriched,
        }
