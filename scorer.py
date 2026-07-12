"""Translation quality scoring."""

from __future__ import annotations

from typing import Any


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def score_translation(
    used_terms: list[dict[str, Any]],
    memory_matches: list[dict[str, Any]],
    document_context: list[dict[str, Any]],
) -> dict[str, float]:
    terminology_score = clamp(len(used_terms) / 5.0)

    memory_score = 0.0
    if memory_matches:
        memory_score = clamp(float(memory_matches[0].get("score", 0.0)))

    context_score = 0.0
    if document_context:
        context_score = clamp(float(document_context[0].get("score", 0.0)))

    total = (
        0.40 * terminology_score
        + 0.35 * memory_score
        + 0.25 * context_score
    )

    return {
        "terminology_score": round(terminology_score, 6),
        "memory_score": round(memory_score, 6),
        "context_score": round(context_score, 6),
        "total_score": round(clamp(total), 6),
    }
