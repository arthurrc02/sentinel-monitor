from datetime import datetime

from pydantic import BaseModel


class MetricSample(BaseModel):
    """Uma amostra de métricas coletada localmente. Espelha o schema `MetricCreate` do backend."""

    cpu_percent: float
    memory_percent: float
    disk_percent: float
    collected_at: datetime
