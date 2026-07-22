from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import ComputerAlreadyExistsError, ComputerNotFoundError


def register_exception_handlers(app: FastAPI) -> None:
    """Traduz exceções de domínio em respostas HTTP.

    Mantém services e repositories livres de qualquer dependência do FastAPI.
    """

    @app.exception_handler(ComputerAlreadyExistsError)
    def handle_computer_already_exists(
        _request: Request, exc: ComputerAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": str(exc)})

    @app.exception_handler(ComputerNotFoundError)
    def handle_computer_not_found(_request: Request, exc: ComputerNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exc)})
