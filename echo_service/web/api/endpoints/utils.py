from typing import Union

from echo_service.db.models.endpoint import Endpoint
from echo_service.web.api.endpoints.schemas.base import (
    Attributes,
    DataResponse,
    DataTypes,
    Response,
)


def build_endpoint_data(endpoint: Endpoint) -> DataResponse:

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

    return ep_data  # noqa: WPS331


def make_endpoint_name(endpoint_id: Union[int, str]) -> str:
    return f"endpoint_{endpoint_id}"
