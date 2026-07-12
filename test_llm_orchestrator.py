from backend.llm.orchestrator import LLMTranslationOrchestrator


def test_llm_orchestrated_translation() -> None:
    orchestrator = LLMTranslationOrchestrator()
    result = orchestrator.translate(
        text="DNA contains genetic information.",
        domain="biology",
        provider="local",
    )
    assert result["translated_text"]
    assert result["llm_provider"] == "local"
    assert result["log_id"]
