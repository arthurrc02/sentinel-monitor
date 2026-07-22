from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.routers import computers, health, metrics

app = FastAPI(title=settings.app_name, version=settings.version)

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(computers.router)
app.include_router(metrics.router)
