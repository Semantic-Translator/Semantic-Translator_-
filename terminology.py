"""Terminology loading and lookup utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DICTIONARIES_ROOT = PROJECT_ROOT / "dictionaries"


def load_dictionary(domain: str, source_language: str, target_language: str) -> dict[str, Any]:
    path = DICTIONARIES_ROOT / domain / f"terms_{source_language}_{target_language}.json"

    if not path.exists():
        return {
            "metadata": {
                "domain": domain,
                "source_language": source_language,
                "target_language": target_language,
                "version": "unknown",
            },
            "terms": [],
        }

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def search_terms(
    query: str,
    domain: str,
    source_language: str = "en",
    target_language: str = "ru",
) -> list[dict[str, Any]]:
    dictionary = load_dictionary(domain, source_language, target_language)
    normalized = query.strip().casefold()

    if not normalized:
        return dictionary.get("terms", [])

    results: list[dict[str, Any]] = []

    for term in dictionary.get("terms", []):
        searchable_values = [
            str(term.get("semantic_id", "")),
            str(term.get("source", "")),
            str(term.get("target", "")),
            str(term.get("definition", "")),
        ]

        if any(normalized in value.casefold() for value in searchable_values):
            results.append(term)

    return results


def apply_terminology(
    text: str,
    domain: str,
    source_language: str = "en",
    target_language: str = "ru",
) -> tuple[str, list[dict[str, Any]]]:
    dictionary = load_dictionary(domain, source_language, target_language)
    translated = text
    used_terms: list[dict[str, Any]] = []

    terms = sorted(
        dictionary.get("terms", []),
        key=lambda item: len(str(item.get("source", ""))),
        reverse=True,
    )

    for term in terms:
        source = str(term.get("source", "")).strip()
        target = str(term.get("target", "")).strip()

        if not source or not target:
            continue

        pattern = re_compile_phrase(source)
        translated, count = pattern.subn(target, translated)

        if count:
            used_terms.append(
                {
                    "semantic_id": term.get("semantic_id"),
                    "source": source,
                    "target": target,
                    "replacements": count,
                }
            )

    return translated, used_terms


def re_compile_phrase(phrase: str):
    import re

    return re.compile(rf"\b{re.escape(phrase)}\b", flags=re.IGNORECASE)
