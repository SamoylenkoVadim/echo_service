from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response
from starlette.routing import Route

from echo_service.constants import MEDIA_TYPE
from echo_service.db.dependencies import get_db_session
from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.endpoints.patch.schemas.request import MessageRequest
from echo_service.web.api.endpoints.patch.schemas.response import MessageResponse
from echo_service.web.api.endpoints.utils import build_endpoint_data, make_endpoint_name
from echo_service.web.shered_app import shared_app

router = APIRouter()


@router.patch("/endpoints/{endpoint_id}", response_model=MessageResponse)
async def edit_endpoint(  # noqa: C901, WPS231
    endpoint_id: int,
    request: Request,
    incoming_message: MessageRequest,
    db: AsyncSession = Depends(get_db_session),
) -> Response:

    endpoint: Optional[Endpoint] = await db.get(Endpoint, endpoint_id)
    if not endpoint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Endpoint with ID '{endpoint_id}' not found",
        )

    # Update the endpoint attributes with the provided values
    data = incoming_message.data
    attributes = data.attributes

    if attributes.verb:
        endpoint.verb = attributes.verb.value  # type: ignore
    if attributes.path:
        endpoint.path = attributes.path  # type: ignore
    if attributes.response and attributes.response.code:
        endpoint.response_code = attributes.response.code  # type: ignore
    if attributes.response and attributes.response.headers:
        endpoint.response_headers = attributes.response.headers  # type: ignore
    if attributes.response and attributes.response.body:
        endpoint.response_body = attributes.response.body  # type: ignore

    await db.flush()

    # Update the route in the app's routes
    app = shared_app.extract()
    target_route = None
    for route in app.routes:
        if isinstance(route, Route) and route.name == make_endpoint_name(endpoint_id):
            target_route = route
            break

    if not target_route:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Route for Endpoint with ID '{endpoint_id}' not found",
        )

    async def dynamic_route(req: Request) -> JSONResponse:
        return JSONResponse(
            content=endpoint.get_body,  # type: ignore
            status_code=endpoint.get_code,  # type: ignore
            headers=endpoint.get_headers,  # type: ignore
        )

    app = shared_app.extract()
    app.routes.remove(target_route)
    app.add_route(
        endpoint.get_path,
        dynamic_route,
        methods=[endpoint.verb],  # type: ignore
        name=make_endpoint_name(endpoint.get_id),
    )

    await db.commit()
    await db.refresh(endpoint)

    endpoint_data = build_endpoint_data(endpoint)
    status_code = status.HTTP_200_OK
    content = MessageResponse(data=endpoint_data).dict()  # type: ignore

    return JSONResponse(
        status_code=status_code,
        content=content,
        media_type=MEDIA_TYPE,
    )
