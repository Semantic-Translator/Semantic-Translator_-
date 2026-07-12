"""Prompt assembly for profile-oriented translation."""

from __future__ import annotations

from typing import Any


def format_terms(terms: list[dict[str, Any]]) -> str:
    if not terms:
        return "No approved terminology context."

    lines = []
    for item in terms:
        lines.append(
            f"- {item.get('semantic_id', '')}: "
            f"{item.get('source', '')} → {item.get('target', '')}; "
            f"{item.get('definition', '')}"
        )
    return "\n".join(lines)


def format_memory(matches: list[dict[str, Any]]) -> str:
    if not matches:
        return "No previous translation-memory matches."

    lines = []
    for item in matches:
        lines.append(
            f"- score={item.get('score', 0)} | "
            f"{item.get('source_text', '')} → {item.get('target_text', '')}"
        )
    return "\n".join(lines)


def format_documents(chunks: list[dict[str, Any]]) -> str:
    if not chunks:
        return "No document context."

    lines = []
    for item in chunks:
        lines.append(
            f"[{item.get('title', '')}#{item.get('chunk_number', '')}] "
            f"{item.get('text', '')}"
        )
    return "\n\n".join(lines)


def build_translation_prompt(
    *,
    source_text: str,
    source_language: str,
    target_language: str,
    domain: str,
    profile: str,
    terminology_context: list[dict[str, Any]],
    memory_matches: list[dict[str, Any]],
    document_context: list[dict[str, Any]],
    deterministic_candidate: str,
) -> str:
    return f"""You are a profile-oriented scientific translator.

SOURCE LANGUAGE: {source_language}
TARGET LANGUAGE: {target_language}
DOMAIN: {domain}
PROFILE: {profile}

RULES:
1. Preserve scientific meaning.
2. Preserve approved terminology.
3. Preserve formulas, units, abbreviations and references.
4. Do not invent facts.
5. Prefer approved translation memory when highly relevant.
6. Use retrieved context only when it supports the source text.

SOURCE TEXT:
{source_text}

APPROVED TERMINOLOGY:
{format_terms(terminology_context)}

TRANSLATION MEMORY:
{format_memory(memory_matches)}

RETRIEVED DOCUMENT CONTEXT:
{format_documents(document_context)}

DETERMINISTIC CANDIDATE:
{deterministic_candidate}

Return only the final translation.

FINAL_TRANSLATION:
{deterministic_candidate}
"""
