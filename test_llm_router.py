from backend.llm.router import ProviderRouter


def test_local_provider() -> None:
    router = ProviderRouter.from_name("local")
    result = router.generate("FINAL_TRANSLATION:\nТестовый перевод")
    assert result.text == "Тестовый перевод"
    assert result.provider == "local"


def test_http_fallback() -> None:
    router = ProviderRouter.from_name("http")
    result = router.generate("FINAL_TRANSLATION:\nРезервный перевод")
    assert result.text == "Резервный перевод"
    assert result.metadata.get("fallback_used") is True
