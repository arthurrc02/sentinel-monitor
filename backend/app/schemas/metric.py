from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MetricCreate(BaseModel):
    """Dados necessários para registrar uma amostra de métricas."""

    cpu_percent: float = Field(ge=0, le=100)
    memory_percent: float = Field(ge=0, le=100)
    disk_percent: float = Field(ge=0, le=100)
    collected_at: datetime


class MetricRead(BaseModel):
    """Representação de uma amostra de métricas retornada pela API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    computer_id: int
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    collected_at: datetime
    created_at: datetime
