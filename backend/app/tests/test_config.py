import pytest

from app.config import get_settings
from app.services.ai_client import OpenAICompatibleAIClient, RuleBasedAIClient, get_ai_client


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_settings_read_openai_key_from_environment(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-value")
    monkeypatch.setenv("LLM_MODEL", "test-model")

    settings = get_settings()

    assert settings.openai_api_key == "sk-test-value"
    assert settings.llm_model == "test-model"


def test_ai_client_uses_openai_client_when_real_key_configured(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-value")

    assert isinstance(get_ai_client(), OpenAICompatibleAIClient)


def test_ai_client_uses_rule_based_client_without_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "")

    assert isinstance(get_ai_client(), RuleBasedAIClient)
