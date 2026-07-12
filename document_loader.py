import csv
import json
from pathlib import Path
from typing import Any

SUPPORTED_EXTENSIONS = {".txt", ".md", ".json", ".csv"}

def flatten_json(value: Any) -> list[str]:
    if isinstance(value, dict):
        out = []
        for key, item in value.items():
            out.append(str(key))
            out.extend(flatten_json(item))
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            out.extend(flatten_json(item))
        return out
    return [str(value)]

def load_document(path: Path) -> str:
    ext = path.suffix.casefold()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported extension: {ext}")
    if ext in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if ext == ".json":
        return " ".join(flatten_json(json.loads(path.read_text(encoding="utf-8"))))
    rows = []
    with path.open("r", encoding="utf-8", newline="") as file:
        for row in csv.reader(file):
            rows.append(" | ".join(row))
    return "\n".join(rows)
