import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ComputerAlreadyExistsError
from app.models.computer import Computer
from app.repositories.computer_repository import ComputerRepository
from app.services.computer_service import ComputerService


def test_register_raises_conflict_on_race_condition(
    db_session: Session, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Simula duas requisições concorrentes: o check de `get_by_hostname` não vê o hostname
    que outra requisição já commitou, e só o `IntegrityError` do banco pega a duplicata.
    """
    repository = ComputerRepository(db_session)
    service = ComputerService(repository)

    def _create_raises_integrity_error(hostname: str) -> Computer:
        raise IntegrityError("INSERT", {}, Exception("UNIQUE constraint failed"))

    monkeypatch.setattr(repository, "create", _create_raises_integrity_error)

    with pytest.raises(ComputerAlreadyExistsError):
        service.register("pc-01")


def test_repository_create_raises_integrity_error_on_duplicate_hostname(
    db_session: Session,
) -> None:
    repository = ComputerRepository(db_session)
    repository.create("pc-01")

    with pytest.raises(IntegrityError):
        repository.create("pc-01")
