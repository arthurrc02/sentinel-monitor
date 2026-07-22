from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Endpoint de verificação de disponibilidade da API."""
    return {"status": "ok"}
