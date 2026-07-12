"""Translation feedback storage."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FEEDBACK_PATH = PROJECT_ROOT / "storage" / "feedback" / "feedback.json"


class FeedbackStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or DEFAULT_FEEDBACK_PATH

    def _load(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8")).get("records", [])

    def add(
        self,
        source_text: str,
        generated_text: str,
        corrected_text: str,
        rating: int,
        domain: str,
        comment: str = "",
    ) -> dict[str, Any]:
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")

        records = self._load()
        record = {
            "feedback_id": str(uuid.uuid4()),
            "source_text": source_text,
            "generated_text": generated_text,
            "corrected_text": corrected_text,
            "rating": rating,
            "domain": domain,
            "comment": comment,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        records.append(record)

        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"version": "0.4.0", "records": records}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        return record
