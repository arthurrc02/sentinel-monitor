from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.metric import Metric
from app.schemas.metric import MetricCreate


class MetricRepository:
    """Acesso a dados de métricas. Não contém regra de negócio."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, computer_id: int, data: MetricCreate) -> Metric:
        metric = Metric(computer_id=computer_id, **data.model_dump())
        self._db.add(metric)
        self._db.commit()
        self._db.refresh(metric)
        return metric

    def list_by_computer(self, computer_id: int, limit: int) -> list[Metric]:
        statement = (
            select(Metric)
            .where(Metric.computer_id == computer_id)
            .order_by(Metric.collected_at.desc())
            .limit(limit)
        )
        return list(self._db.scalars(statement))
