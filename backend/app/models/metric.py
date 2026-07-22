from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.computer import Computer


class Metric(Base):
    """Uma amostra de métricas de um computador em um instante específico."""

    __tablename__ = "metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    computer_id: Mapped[int] = mapped_column(ForeignKey("computers.id"), index=True)
    cpu_percent: Mapped[float]
    memory_percent: Mapped[float]
    disk_percent: Mapped[float]
    collected_at: Mapped[datetime]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    computer: Mapped["Computer"] = relationship(back_populates="metrics")
