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
    computers = service.list_computers()
    return [ComputerRead.model_validate(computer) for computer in computers]
