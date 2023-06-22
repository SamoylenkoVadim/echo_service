from typing import List

from pydantic import BaseModel

from echo_service.web.api.endpoints.schemas.base import DataResponse


class MessageResponseAllEndpoints(BaseModel):
    data: List[DataResponse]
