from datetime import datetime

from pydantic import BaseModel


class Computer(BaseModel):
    """Espelha o schema `ComputerRead` do backend."""

    id: int
    hostname: str
    created_at: datetime
