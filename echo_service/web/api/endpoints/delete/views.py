from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.routing import Route

from echo_service.db.dependencies import get_db_session
from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.endpoints.utils import make_endpoint_name
from echo_service.web.shered_app import shared_app

router = APIRouter()


@router.delete("/endpoints/{endpoint_id}")
async def delete_endpoint(
    endpoint_id: int,
    db: AsyncSession = Depends(get_db_session),
) -> Response:

    endpoint_name = make_endpoint_name(endpoint_id)
    app = shared_app.extract()

    # Find the target route with matching name in the app's router
    target_route = None
    for route in app.routes:
        if isinstance(route, Route) and route.name == endpoint_name:
            target_route = route
            break

    endpoint = await db.get(Endpoint, endpoint_id)

    # Check if the endpoint exists in the database and in the app router
    if endpoint is None and target_route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Endpoint with ID '{endpoint_id}' not found",
        )

    # Delete the endpoint from the database if exists
    if endpoint:
        await db.delete(endpoint)
        await db.commit()

    # Remove the route from the app's routes if exists
    if target_route:
        app.routes.remove(target_route)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
