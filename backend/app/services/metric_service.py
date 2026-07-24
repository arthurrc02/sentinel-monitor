import logging

from app.core.exceptions import ComputerNotFoundError
from app.models.metric import Metric
from app.repositories.computer_repository import ComputerRepository
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate

logger = logging.getLogger(__name__)


class MetricService:
    """Regras de negócio para registro e consulta de métricas."""

    def __init__(
        self, computer_repository: ComputerRepository, metric_repository: MetricRepository
    ) -> None:
        self._computer_repository = computer_repository
        self._metric_repository = metric_repository

    def record_metric(self, computer_id: int, data: MetricCreate) -> Metric:
        self._ensure_computer_exists(computer_id)
        metric = self._metric_repository.create(computer_id, data)
        logger.info("métrica registrada: computer_id=%s metric_id=%s", computer_id, metric.id)
        return metric

    def list_history(self, computer_id: int, limit: int) -> list[Metric]:
        self._ensure_computer_exists(computer_id)
        return self._metric_repository.list_by_computer(computer_id, limit)

    def _ensure_computer_exists(self, computer_id: int) -> None:
        if self._computer_repository.get_by_id(computer_id) is None:
            logger.warning("referência a computador inexistente: computer_id=%s", computer_id)
            raise ComputerNotFoundError(computer_id)
