import logging
from datetime import UTC, datetime, timedelta
from typing import NamedTuple

from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.core.exceptions import ComputerAlreadyExistsError
from app.models.computer import Computer
from app.repositories.computer_repository import ComputerRepository

logger = logging.getLogger(__name__)


class ComputerStatus(NamedTuple):
    """Um computador junto com sua disponibilidade calculada no momento da consulta."""

    computer: Computer
    last_seen_at: datetime | None
    is_online: bool


class ComputerService:
    """Regras de negócio para registro e consulta de computadores."""

    def __init__(self, computer_repository: ComputerRepository) -> None:
        self._computer_repository = computer_repository

    def register(self, hostname: str) -> Computer:
        if self._computer_repository.get_by_hostname(hostname) is not None:
            logger.info("tentativa de registrar hostname já existente: %s", hostname)
            raise ComputerAlreadyExistsError(hostname)
        try:
            computer = self._computer_repository.create(hostname)
        except IntegrityError:
            # Corrida entre requisições simultâneas com o mesmo hostname: o check acima
            # passou para as duas, mas só uma consegue inserir; a outra vira 409 limpo.
            logger.info("corrida ao registrar hostname já existente: %s", hostname)
            raise ComputerAlreadyExistsError(hostname) from None
        logger.info("computador registrado: id=%s hostname=%s", computer.id, hostname)
        return computer

    def list_computers(self) -> list[ComputerStatus]:
        threshold = timedelta(seconds=settings.offline_threshold_seconds)
        now = datetime.now(UTC)
        return [
            ComputerStatus(computer, last_seen_at, _is_online(last_seen_at, now, threshold))
            for computer, last_seen_at in self._computer_repository.list_all_with_last_seen()
        ]


def _is_online(last_seen_at: datetime | None, now: datetime, threshold: timedelta) -> bool:
    """Um computador é online se já reportou métricas dentro da janela de tolerância."""
    if last_seen_at is None:
        return False
    if last_seen_at.tzinfo is None:
        last_seen_at = last_seen_at.replace(tzinfo=UTC)
    return now - last_seen_at <= threshold
