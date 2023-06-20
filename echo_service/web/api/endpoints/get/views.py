from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from echo_service.constants import MEDIA_TYPE
from echo_service.db.dependencies import get_db_session
from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.endpoints.get.schemas.response import MessageResponse
from echo_service.web.api.endpoints.schemas.base import (
    Attributes,
    DataResponse,
    DataTypes,
    Response,
)

router = APIRouter()


@router.get("/endpoints", response_model=MessageResponse)
async def create_endpoint(
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:

    endpoints = await db.execute(select(Endpoint))
    endpoint_data = []

    for endpoint in endpoints.scalars():
        ep_response = Response(
            code=endpoint.get_code,
            headers=endpoint.get_headers,
            body=endpoint.get_body,
        )
        ep_attributes = Attributes(
            verb=endpoint.get_verb,  # type: ignore
            path=endpoint.get_path,
            response=ep_response,
        )
        ep_data = DataResponse(
            id=endpoint.get_id,  # type: ignore
            type=DataTypes.endpoints.value,  # type: ignore
            attributes=ep_attributes,
        )
        endpoint_data.append(ep_data)

    status_code = status.HTTP_200_OK
    content = MessageResponse(data=endpoint_data).dict()

    return JSONResponse(
        status_code=status_code,
        content=content,
        media_type=MEDIA_TYPE,
    )
