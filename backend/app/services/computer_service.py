from app.core.exceptions import ComputerAlreadyExistsError
from app.models.computer import Computer
from app.repositories.computer_repository import ComputerRepository


class ComputerService:
    """Regras de negócio para registro e consulta de computadores."""

    def __init__(self, computer_repository: ComputerRepository) -> None:
        self._computer_repository = computer_repository

    def register(self, hostname: str) -> Computer:
        if self._computer_repository.get_by_hostname(hostname) is not None:
            raise ComputerAlreadyExistsError(hostname)
        return self._computer_repository.create(hostname)

    def list_computers(self) -> list[Computer]:
        return self._computer_repository.list_all()
