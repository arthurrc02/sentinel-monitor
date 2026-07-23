from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.computer import Computer
from app.models.metric import Metric


class ComputerRepository:
    """Acesso a dados de computadores. Não contém regra de negócio."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, hostname: str) -> Computer:
        computer = Computer(hostname=hostname)
        self._db.add(computer)
        self._db.commit()
        self._db.refresh(computer)
        return computer

    def get_by_id(self, computer_id: int) -> Computer | None:
        return self._db.get(Computer, computer_id)

    def get_by_hostname(self, hostname: str) -> Computer | None:
        return self._db.scalar(select(Computer).where(Computer.hostname == hostname))

    def list_all_with_last_seen(self) -> list[tuple[Computer, datetime | None]]:
        """Cada computador junto com o `collected_at` da métrica mais recente (ou `None`)."""
        last_seen_subquery = (
            select(Metric.computer_id, func.max(Metric.collected_at).label("last_seen_at"))
            .group_by(Metric.computer_id)
            .subquery()
        )
        statement = (
            select(Computer, last_seen_subquery.c.last_seen_at)
            .outerjoin(last_seen_subquery, Computer.id == last_seen_subquery.c.computer_id)
            .order_by(Computer.hostname)
        )
        return list(self._db.execute(statement).tuples())
