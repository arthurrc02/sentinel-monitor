from fastapi import APIRouter, status

from app.core.dependencies import ComputerServiceDep
from app.schemas.computer import ComputerCreate, ComputerRead

router = APIRouter(prefix="/computers", tags=["computers"])


@router.post("", response_model=ComputerRead, status_code=status.HTTP_201_CREATED)
def register_computer(data: ComputerCreate, service: ComputerServiceDep) -> ComputerRead:
    computer = service.register(data.hostname)
    return ComputerRead.model_validate(computer)


@router.get("", response_model=list[ComputerRead])
def list_computers(service: ComputerServiceDep) -> list[ComputerRead]:
    computer_statuses = service.list_computers()
    return [
        ComputerRead(
            id=computer_status.computer.id,
            hostname=computer_status.computer.hostname,
            created_at=computer_status.computer.created_at,
            last_seen_at=computer_status.last_seen_at,
            is_online=computer_status.is_online,
        )
        for computer_status in computer_statuses
    ]
