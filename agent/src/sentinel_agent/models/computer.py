from datetime import datetime

from pydantic import BaseModel


class Computer(BaseModel):
    """Só os campos de `ComputerRead` (backend) que o Agent realmente usa.

    O backend também retorna `last_seen_at`/`is_online`, mas o Agent nunca precisa
    ler esses dois — Pydantic ignora campos extras da resposta por padrão.
    """

    id: int
    hostname: str
    created_at: datetime
