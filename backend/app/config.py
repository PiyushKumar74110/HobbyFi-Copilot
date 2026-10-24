
"""Application configuration for HobbyFi Copilot."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Define and load application settings."""

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

    # Application
    APP_NAME: str = "HobbyFi Copilot"
    ENVIRONMENT: str = "development"

    # Database
    DATABASE_URL: str

    # LLM
    LLM_PROVIDER: str = "ollama"

    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"

    OPENAI_MODEL: str = "gpt-5"

    GEMINI_MODEL: str = "gemini-3.1-pro-preview"

    GOOGLE_API_KEY: str | None = None

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Vector DB
    VECTOR_DB_PATH: str = "vector_db/chroma"


settings = Settings()
