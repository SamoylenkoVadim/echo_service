from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from echo_service.constants import MEDIA_TYPE
from echo_service.db.dependencies import get_db_session
from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.endpoints.get.schemas.response import (
    MessageResponseAllEndpoints,
)
from echo_service.web.api.endpoints.utils import build_endpoint_data

router = APIRouter()


@router.get("/endpoints", response_model=MessageResponseAllEndpoints)
async def create_endpoint(
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:

    endpoints = await db.execute(select(Endpoint))
    endpoint_data = []

    for endpoint in endpoints.scalars():
        ep_data = build_endpoint_data(endpoint)
        endpoint_data.append(ep_data)

    status_code = status.HTTP_200_OK
    content = MessageResponseAllEndpoints(data=endpoint_data).dict()

    return JSONResponse(
        status_code=status_code,
        content=content,
        media_type=MEDIA_TYPE,
    )
