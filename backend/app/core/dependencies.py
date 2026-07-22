from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.computer_repository import ComputerRepository
from app.repositories.metric_repository import MetricRepository
from app.services.computer_service import ComputerService
from app.services.metric_service import MetricService

DbSession = Annotated[Session, Depends(get_db)]


def get_computer_repository(db: DbSession) -> ComputerRepository:
    return ComputerRepository(db)


def get_metric_repository(db: DbSession) -> MetricRepository:
    return MetricRepository(db)


ComputerRepositoryDep = Annotated[ComputerRepository, Depends(get_computer_repository)]
MetricRepositoryDep = Annotated[MetricRepository, Depends(get_metric_repository)]


def get_computer_service(computer_repository: ComputerRepositoryDep) -> ComputerService:
    return ComputerService(computer_repository)


def get_metric_service(
    computer_repository: ComputerRepositoryDep, metric_repository: MetricRepositoryDep
) -> MetricService:
    return MetricService(computer_repository, metric_repository)


ComputerServiceDep = Annotated[ComputerService, Depends(get_computer_service)]
MetricServiceDep = Annotated[MetricService, Depends(get_metric_service)]
