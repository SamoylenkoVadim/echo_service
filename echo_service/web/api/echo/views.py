from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from echo_service.constants import LOCATION_HEADER, MEDIA_TYPE
from echo_service.db.dependencies import get_db_session
from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.easy_app import get_easy_app
from echo_service.web.api.echo.schemas.request import DataTypes, MessageRequest
from echo_service.web.api.echo.schemas.response import DataResponse, MessageResponse

router = APIRouter()


@router.post("/endpoints", response_model=MessageResponse)
async def create_endpoint(
    request: Request,
    incoming_message: MessageRequest,
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:

    data = incoming_message.data
    attributes = data.attributes

    existing_endpoint = await db.execute(
        select(Endpoint).where(
            and_(
                Endpoint.verb == attributes.verb.value,
                Endpoint.path == attributes.path,
            ),
        ),
    )

    if existing_endpoint.scalar() or attributes.path == "/endpoints":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Endpoint with the same verb and path already exists",
        )

    endpoint = Endpoint(
        verb=attributes.verb.value,
        path=attributes.path,
        response_code=attributes.response.code,
        response_headers=attributes.response.headers,
        response_body=attributes.response.body,
    )
    db.add(endpoint)
    await db.flush()

    async def dynamic_route(request: Request) -> JSONResponse:
        return JSONResponse(
            content={},
            status_code=status.HTTP_200_OK,
        )

    easy_app = get_easy_app()
    easy_app.add_route(
        attributes.path,
        dynamic_route,
        methods=[attributes.verb.value],
        name=str(endpoint.id),
    )

    endpoint_data = DataResponse(
        id=str(endpoint.id),
        type=DataTypes.endpoints,
        attributes=attributes,
    )

    status_code = status.HTTP_201_CREATED
    content = MessageResponse(data=endpoint_data).dict()
    current_url = str(request.base_url)[:-1]
    headers = {LOCATION_HEADER: f"{current_url}{endpoint.path}"}

    await db.commit()
    await db.refresh(endpoint)

    return JSONResponse(
        status_code=status_code,
        content=content,
        headers=headers,
        media_type=MEDIA_TYPE,
    )
