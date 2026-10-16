from gulzar_text_utils import normalize_text
from gulzar_logging_utils import get_logger


def test_normalize_text_collapses_whitespace():
    assert normalize_text("  hello   Kotlin1 \n Python  ") == "hello Kotlin1 Python"


def test_normalize_text_handles_empty_input():
    assert normalize_text("   ") == ""


def test_get_logger_uses_requested_name():
    logger = get_logger("kotlin1-python-service-test")
    assert logger.name == "kotlin1-python-service-test"
