from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.computer import Computer


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

    def list_all(self) -> list[Computer]:
        return list(self._db.scalars(select(Computer).order_by(Computer.hostname)))
