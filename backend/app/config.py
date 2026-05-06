import os
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


_ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(_ENV_PATH, override=False)


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


def _float_env(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if raw_value is None or raw_value == "":
        return default
    return float(raw_value)


def _list_env(name: str, default: str) -> list[str]:
    raw_value = os.getenv(name, default)
    return [value.strip() for value in raw_value.split(",") if value.strip()]


@dataclass(frozen=True)
class Settings:
    app_name: str = field(default_factory=lambda: _env("APP_NAME", "TriagePilot AI"))
    database_url: str = field(default_factory=lambda: _env("DATABASE_URL", "sqlite:///./support_tickets.db"))
    chroma_path: str = field(default_factory=lambda: _env("CHROMA_PATH", "./chroma_db"))
    cors_allowed_origins: list[str] = field(
        default_factory=lambda: _list_env(
            "CORS_ALLOWED_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000",
        ),
    )
    similarity_threshold: float = field(default_factory=lambda: _float_env("SIMILARITY_THRESHOLD", 0.70))
    openai_api_key: str = field(default_factory=lambda: _env("OPENAI_API_KEY", ""))
    openai_base_url: str = field(default_factory=lambda: _env("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    llm_model: str = field(default_factory=lambda: _env("LLM_MODEL", "gpt-4.1-mini"))
    embedding_model: str = field(default_factory=lambda: _env("EMBEDDING_MODEL", "text-embedding-3-small"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
