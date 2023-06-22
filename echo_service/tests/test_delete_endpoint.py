from typing import AsyncGenerator

import pytest
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.endpoints.utils import make_endpoint_name


@pytest.mark.anyio
async def test_delete_endpoint(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:
    # Setup
    endpoint_id = 1
    endpoint_name = make_endpoint_name(endpoint_id)
    mock_endpoint = Endpoint(
        id=endpoint_id,
        verb="GET",
        path="/123",
        response_code=200,
        response_headers={},
        response_body="response_body",
    )

    dbsession.add(mock_endpoint)  # type: ignore
    await dbsession.commit()  # type: ignore

    async def dynamic_route(req: Request) -> JSONResponse:
        return JSONResponse(
            content=mock_endpoint.get_body,
            headers=mock_endpoint.get_headers,
            status_code=mock_endpoint.get_code,
        )

    fastapi_app.add_route(
        mock_endpoint.get_path,
        dynamic_route,
        methods=[mock_endpoint.get_verb],
        name=make_endpoint_name(mock_endpoint.get_id),
    )

    url = fastapi_app.url_path_for("delete_endpoint", endpoint_id=endpoint_id)
    response = await client.delete(url)

    # Assert
    deleted_endpoint = await dbsession.get(Endpoint, endpoint_id)  # type: ignore
    assert deleted_endpoint is None
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not any(
        route for route in fastapi_app.routes if route.name == endpoint_name  # type: ignore # noqa: E501
    )


@pytest.mark.anyio
async def test_delete_endpoint_not_found(
    client: AsyncClient,
    dbsession: AsyncGenerator[AsyncSession, None],
    fastapi_app: FastAPI,
) -> None:
    # Setup
    endpoint_id = 3

    # Call
    url = fastapi_app.url_path_for("delete_endpoint", endpoint_id=endpoint_id)
    response = await client.delete(url)

    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert f"Endpoint with ID '{endpoint_id}' not found" in response.text
