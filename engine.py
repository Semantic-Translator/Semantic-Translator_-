"""Base translation engine.

Version 0.1.0 contains only the interface.
Real translation logic will be added in the next archive.
"""


class TranslationEngine:
    def translate(
        self,
        text: str,
        source_language: str,
        target_language: str,
        domain: str,
    ) -> str:
        if not text.strip():
            raise ValueError("Text must not be empty.")

        return text
