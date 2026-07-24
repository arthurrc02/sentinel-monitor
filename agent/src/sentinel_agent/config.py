from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações do agent, carregadas de variáveis de ambiente ou .env."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SENTINEL_")

    api_base_url: str = "http://localhost:8000"
    hostname: str | None = None
    collection_interval_seconds: float = 60.0
    request_timeout_seconds: float = 10.0
    max_retry_attempts: int = 5
    retry_base_delay_seconds: float = 1.0
    log_level: str = "INFO"
    disk_path: str = "/"


settings = Settings()
