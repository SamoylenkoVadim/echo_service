from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from echo_service.db.dependencies import get_db_session
from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.echo.schemas.request import DataTypes, Request
from echo_service.web.api.echo.schemas.response import Data, Response

router = APIRouter()


@router.post("/endpoints", response_model=Response)
async def create_endpoint(
    incoming_message: Request,
    db: AsyncSession = Depends(get_db_session),
) -> Response:

    data = incoming_message.data
    attributes = data.attributes

    endpoint = Endpoint(
        verb=attributes.verb.value,
        path=attributes.path,
        response_code=attributes.response.code,
        response_headers=attributes.response.headers,
        response_body=attributes.response.body,
    )

    db.add(endpoint)
    await db.commit()
    await db.refresh(endpoint)

    response_data = Data(
        id=str(endpoint.id),
        type=DataTypes.endpoints,
        attributes=attributes,
    )

    return Response(data=response_data)
