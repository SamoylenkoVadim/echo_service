from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from echo_service.constants import LOCATION_HEADER, MEDIA_TYPE
from echo_service.db.dependencies import get_db_session
from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.endpoints.post.schemas.request import MessageRequest
from echo_service.web.api.endpoints.post.schemas.response import (
    DataResponse,
    MessageResponse,
)
from echo_service.web.api.endpoints.schemas.base import DataTypes
from echo_service.web.shered_app import shared_app
from echo_service.web.utils import make_endpoint_name

router = APIRouter()


@router.post("/endpoints", response_model=MessageResponse)
async def create_endpoint(
    request: Request,
    incoming_message: MessageRequest,
    db: AsyncSession = Depends(get_db_session),
) -> JSONResponse:

    # Extract data and attributes from the incoming message
    data = incoming_message.data
    attributes = data.attributes

    # Check if an endpoint with the same verb and path already exists
    existing_endpoint = await db.execute(
        select(Endpoint).where(
            and_(
                Endpoint.verb == attributes.verb.value,
                Endpoint.path == attributes.path,
            ),
        ),
    )

    # If an endpoint already exists or the path is "/endpoints", raise an exception
    if existing_endpoint.scalar() or attributes.path == "/endpoints":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Endpoint with the same verb and path already exists",
        )

    # Create a new Endpoint object and save it into DB, but without commit in order to
    # have an option to do a rollback
    endpoint = Endpoint(
        verb=attributes.verb.value,
        path=attributes.path,
        response_code=attributes.response.code,
        response_headers=attributes.response.headers,
        response_body=attributes.response.body,
    )
    db.add(endpoint)
    await db.flush()

    # Get an access to the main application and add a dynamic route to it
    app = shared_app.extract()

    async def dynamic_route(req: Request) -> JSONResponse:
        return JSONResponse(
            content=endpoint.get_body,
            headers=endpoint.get_headers,
            status_code=endpoint.get_code,
        )

    app.add_route(
        endpoint.get_path,
        dynamic_route,
        methods=[endpoint.get_verb],
        name=make_endpoint_name(endpoint.get_id),
    )

    # Prepare the response data
    endpoint_data = DataResponse(
        id=str(endpoint.get_id),
        type=DataTypes.endpoints,
        attributes=attributes,
    )
    status_code = status.HTTP_201_CREATED
    content = MessageResponse(data=endpoint_data).dict()
    current_url = str(request.base_url)[:-1]
    headers = {LOCATION_HEADER: f"{current_url}{endpoint.path}"}

    # Commit changes to the database
    await db.commit()
    await db.refresh(endpoint)

    # Return the JSON response with appropriate status code,
    # content, headers, and media type
    return JSONResponse(
        status_code=status_code,
        content=content,
        headers=headers,
        media_type=MEDIA_TYPE,
    )
