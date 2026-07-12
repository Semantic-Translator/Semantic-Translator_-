"""LLM interaction logger."""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_ROOT = PROJECT_ROOT / "storage" / "llm_logs"


def log_generation(
    *,
    provider: str,
    model: str,
    prompt: str,
    output: str,
    metadata: dict[str, Any],
) -> str:
    LOG_ROOT.mkdir(parents=True, exist_ok=True)
    log_id = str(uuid.uuid4())

    record = {
        "log_id": log_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "model": model,
        "prompt": prompt,
        "output": output,
        "metadata": metadata,
    }

    path = LOG_ROOT / f"{log_id}.json"
    path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return log_id
