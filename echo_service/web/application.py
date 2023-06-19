from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from echo_service.web.api.router import api_router
from echo_service.web.lifetime import (
    register_exception_handler,
    register_shutdown_event,
    register_startup_event,
)
from echo_service.web.shered_app import shared_app


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        title="echo_service",
        version=metadata.version("echo_service"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    register_startup_event(app)
    register_shutdown_event(app)
    register_exception_handler(app)

    app.include_router(router=api_router)

    shared_app.save(app)

    return app
