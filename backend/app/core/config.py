from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação, carregadas de variáveis de ambiente ou .env."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SENTINEL_")

    app_name: str = "Sentinel Backend"
    version: str = "0.1.0"
    database_url: str = "postgresql+psycopg://sentinel:sentinel@localhost:5432/sentinel"
    cors_origins: list[str] = ["http://localhost:5173"]


settings = Settings()
