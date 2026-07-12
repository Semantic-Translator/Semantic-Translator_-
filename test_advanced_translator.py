from backend.generation.advanced_translator import AdvancedTranslator


def test_approved_memory_reuse() -> None:
    translator = AdvancedTranslator()
    result = translator.translate(
        "DNA contains genetic information.",
        domain="biology",
        reuse_threshold=0.80,
    )
    assert result["memory_reused"] is True
    assert result["translated_text"] == "ДНК содержит генетическую информацию."
