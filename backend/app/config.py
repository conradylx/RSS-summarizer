from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Reads configuration from .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str
    redis_url: str


settings = Settings()  # type: ignore
