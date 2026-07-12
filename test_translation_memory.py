from pathlib import Path
from tempfile import TemporaryDirectory

from backend.memory.index import TranslationMemory


def test_memory_add_and_search() -> None:
    with TemporaryDirectory() as tmp:
        memory = TranslationMemory(Path(tmp) / "memory.json")
        memory.add(
            source_text="DNA contains genetic information.",
            target_text="ДНК содержит генетическую информацию.",
            source_language="en",
            target_language="ru",
            domain="biology",
            status="approved",
            quality_score=1.0,
        )
        results = memory.search(
            "DNA contains genetic information.",
            domain="biology",
            approved_only=True,
        )
        assert results
        assert results[0]["exact_score"] == 1.0
