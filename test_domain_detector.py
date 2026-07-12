from backend.semantic.domain_detector import detect_domain


def test_detect_biology() -> None:
    assert detect_domain("The cell membrane contains proteins.") == "biology"


def test_detect_common() -> None:
    assert detect_domain("Hello world.") == "common"
