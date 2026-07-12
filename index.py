"""Portable JSON vector index."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from backend.translator.terminology import DICTIONARIES_ROOT
from backend.vector.vectorizer import HashingVectorizer, cosine_similarity


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INDEX_PATH = PROJECT_ROOT / "storage" / "vector_index" / "terms.json"


@dataclass
class VectorRecord:
    semantic_id: str
    domain: str
    source_language: str
    target_language: str
    source: str
    target: str
    definition: str
    search_text: str
    vector: list[float]


class VectorIndex:
    def __init__(
        self,
        index_path: Path | None = None,
        vectorizer: HashingVectorizer | None = None,
    ) -> None:
        self.index_path = index_path or DEFAULT_INDEX_PATH
        self.vectorizer = vectorizer or HashingVectorizer()
        self.records: list[VectorRecord] = []

    @staticmethod
    def _record_text(term: dict[str, Any], domain: str) -> str:
        values = [
            str(term.get("source", "")),
            str(term.get("target", "")),
            str(term.get("definition", "")),
            domain,
            " ".join(term.get("synonyms", [])),
            " ".join(term.get("abbreviations", [])),
        ]
        return " | ".join(value for value in values if value)

    def build(self) -> int:
        records: list[VectorRecord] = []

        for dictionary_path in DICTIONARIES_ROOT.glob("*/terms_*_*.json"):
            with dictionary_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            metadata = data.get("metadata", {})
            domain = str(metadata.get("domain", dictionary_path.parent.name))
            source_language = str(metadata.get("source_language", "unknown"))
            target_language = str(metadata.get("target_language", "unknown"))

            for term in data.get("terms", []):
                search_text = self._record_text(term, domain)
                records.append(
                    VectorRecord(
                        semantic_id=str(term.get("semantic_id", "")),
                        domain=domain,
                        source_language=source_language,
                        target_language=target_language,
                        source=str(term.get("source", "")),
                        target=str(term.get("target", "")),
                        definition=str(term.get("definition", "")),
                        search_text=search_text,
                        vector=self.vectorizer.encode(search_text),
                    )
                )

        self.records = records
        self.save()
        return len(records)

    def save(self) -> None:
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "version": "0.2.0",
            "dimensions": self.vectorizer.config.dimensions,
            "count": len(self.records),
            "records": [asdict(record) for record in self.records],
        }
        self.index_path.write_text(
            json.dumps(payload, ensure_ascii=False),
            encoding="utf-8",
        )

    def load(self) -> int:
        if not self.index_path.exists():
            return self.build()

        data = json.loads(self.index_path.read_text(encoding="utf-8"))
        self.records = [
            VectorRecord(**record)
            for record in data.get("records", [])
        ]
        return len(self.records)

    def search(
        self,
        query: str,
        top_k: int = 5,
        domain: str | None = None,
        minimum_score: float = 0.0,
    ) -> list[dict[str, Any]]:
        if not self.records:
            self.load()

        query_vector = self.vectorizer.encode(query)
        results: list[dict[str, Any]] = []

        for record in self.records:
            if domain and domain != "auto" and record.domain != domain:
                continue

            score = cosine_similarity(query_vector, record.vector)
            if score < minimum_score:
                continue

            results.append({
                "score": round(score, 6),
                "semantic_id": record.semantic_id,
                "domain": record.domain,
                "source_language": record.source_language,
                "target_language": record.target_language,
                "source": record.source,
                "target": record.target,
                "definition": record.definition,
            })

        results.sort(key=lambda item: item["score"], reverse=True)
        return results[:max(1, top_k)]

    def status(self) -> dict[str, Any]:
        if not self.records and self.index_path.exists():
            self.load()

        return {
            "path": str(self.index_path),
            "exists": self.index_path.exists(),
            "records": len(self.records),
            "dimensions": self.vectorizer.config.dimensions,
        }
