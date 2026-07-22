from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(title=settings.app_name, version=settings.version)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Endpoint de verificação de disponibilidade da API."""
    return {"status": "ok"}
