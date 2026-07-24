from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ComputerCreate(BaseModel):
    """Dados necessários para registrar um computador."""

    hostname: str = Field(min_length=1, max_length=255)

    @field_validator("hostname", mode="before")
    @classmethod
    def _strip_hostname(cls, value: object) -> object:
        """Normaliza espaços nas pontas antes da validação de tamanho.

        Evita tratar "pc-01 " como um hostname diferente de "pc-01".
        """
        return value.strip() if isinstance(value, str) else value


class ComputerRead(BaseModel):
    """Representação de um computador retornada pela API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    hostname: str
    created_at: datetime
    last_seen_at: datetime | None = None
    is_online: bool = False
