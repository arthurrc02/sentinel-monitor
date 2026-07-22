from app.core.exceptions import ComputerNotFoundError
from app.models.metric import Metric
from app.repositories.computer_repository import ComputerRepository
from app.repositories.metric_repository import MetricRepository
from app.schemas.metric import MetricCreate


class MetricService:
    """Regras de negócio para registro e consulta de métricas."""

    def __init__(
        self, computer_repository: ComputerRepository, metric_repository: MetricRepository
    ) -> None:
        self._computer_repository = computer_repository
        self._metric_repository = metric_repository

    def record_metric(self, computer_id: int, data: MetricCreate) -> Metric:
        self._ensure_computer_exists(computer_id)
        return self._metric_repository.create(computer_id, data)

    def list_history(self, computer_id: int, limit: int) -> list[Metric]:
        self._ensure_computer_exists(computer_id)
        return self._metric_repository.list_by_computer(computer_id, limit)

    def _ensure_computer_exists(self, computer_id: int) -> None:
        if self._computer_repository.get_by_id(computer_id) is None:
            raise ComputerNotFoundError(computer_id)
