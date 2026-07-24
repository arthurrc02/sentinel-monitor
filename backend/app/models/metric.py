from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.computer import Computer


class Metric(Base):
    """Uma amostra de métricas de um computador em um instante específico."""

    __tablename__ = "metrics"
    __table_args__ = (
        # Cobre tanto "métricas de um computador" (prefixo esquerdo) quanto o cálculo de
        # last_seen_at (MAX(collected_at) por computador) e o histórico ordenado por data.
        Index("ix_metrics_computer_id_collected_at", "computer_id", "collected_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    computer_id: Mapped[int] = mapped_column(ForeignKey("computers.id"))
    cpu_percent: Mapped[float]
    memory_percent: Mapped[float]
    disk_percent: Mapped[float]
    collected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    computer: Mapped["Computer"] = relationship(back_populates="metrics")
