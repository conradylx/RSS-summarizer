from pydantic_settings import BaseSettings, SettingsConfigDict

ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://100.93.37.11:5173",
    "http://100.93.37.11:8080",
]


class Settings(BaseSettings):
    """Reads configuration from .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str
    redis_url: str
    ollama_url: str = "http://ollama:11434/v1"


settings = Settings()  # type: ignore
