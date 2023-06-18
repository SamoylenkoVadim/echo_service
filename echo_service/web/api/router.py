from fastapi.routing import APIRouter

from echo_service.web.api import echo, monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(echo.router, tags=["echo"])
