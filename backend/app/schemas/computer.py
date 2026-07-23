from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ComputerCreate(BaseModel):
    """Dados necessários para registrar um computador."""

    hostname: str = Field(min_length=1, max_length=255)


class ComputerRead(BaseModel):
    """Representação de um computador retornada pela API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    hostname: str
    created_at: datetime
    last_seen_at: datetime | None = None
    is_online: bool = False
