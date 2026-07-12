from backend.translator.terminology import apply_terminology, search_terms


def test_search_biology_term() -> None:
    results = search_terms("membrane", "biology")
    assert results
    assert results[0]["target"] == "клеточная мембрана"


def test_apply_terminology() -> None:
    translated, used_terms = apply_terminology(
        "The cell membrane contains protein.",
        "biology",
    )
    assert "клеточная мембрана" in translated
    assert "белок" in translated
    assert used_terms
