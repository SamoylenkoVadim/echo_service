from fastapi.routing import APIRouter

from echo_service.web.api import monitoring
from echo_service.web.api.endpoints import delete, get, patch, post

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(post.router, tags=["post"])
api_router.include_router(delete.router, tags=["delete"])
api_router.include_router(get.router, tags=["get"])
api_router.include_router(patch.router, tags=["patch"])
