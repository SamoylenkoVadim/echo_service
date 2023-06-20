from pydantic import BaseModel

from echo_service.web.api.endpoints.schemas.base import DataRequest


class MessageRequest(BaseModel):
    data: DataRequest
