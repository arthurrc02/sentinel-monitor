from typing import Annotated

from fastapi import APIRouter, Query, status

from app.core.dependencies import MetricServiceDep
from app.schemas.metric import MetricCreate, MetricRead

router = APIRouter(prefix="/computers/{computer_id}/metrics", tags=["metrics"])


@router.post("", response_model=MetricRead, status_code=status.HTTP_201_CREATED)
def record_metric(computer_id: int, data: MetricCreate, service: MetricServiceDep) -> MetricRead:
    metric = service.record_metric(computer_id, data)
    return MetricRead.model_validate(metric)


@router.get("", response_model=list[MetricRead])
def list_metric_history(
    computer_id: int,
    service: MetricServiceDep,
    limit: Annotated[int, Query(ge=1, le=1000)] = 100,
) -> list[MetricRead]:
    metrics = service.list_history(computer_id, limit)
    return [MetricRead.model_validate(metric) for metric in metrics]
