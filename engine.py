"""Domain-aware translation prototype."""

from __future__ import annotations

from backend.translator.terminology import apply_terminology


class TranslationEngine:
    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
        domain: str,
    ) -> tuple[str, list[dict]]:
        if not text.strip():
            raise ValueError("Text must not be empty.")

        return apply_terminology(
            text=text,
            domain=domain,
            source_language=source_language,
            target_language=target_language,
        )
