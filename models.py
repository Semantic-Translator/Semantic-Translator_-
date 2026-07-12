"""Knowledge graph data models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ConceptNode:
    semantic_id: str
    domain: str
    labels: dict[str, str]
    aliases: dict[str, list[str]] = field(default_factory=dict)
    definition: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    vector: list[float] = field(default_factory=list)


@dataclass
class ConceptRelation:
    relation_id: str
    source_id: str
    relation_type: str
    target_id: str
    confidence: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)
