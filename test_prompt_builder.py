from backend.prompts.builder import build_translation_prompt


def test_prompt_contains_context() -> None:
    prompt = build_translation_prompt(
        source_text="DNA contains genetic information.",
        source_language="en",
        target_language="ru",
        domain="biology",
        profile="scientific",
        terminology_context=[{
            "semantic_id": "BIO-000008",
            "source": "DNA",
            "target": "ДНК",
            "definition": "Genetic material",
        }],
        memory_matches=[],
        document_context=[],
        deterministic_candidate="ДНК contains genetic information.",
    )
    assert "BIO-000008" in prompt
    assert "FINAL_TRANSLATION:" in prompt
