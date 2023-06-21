from pydantic import BaseModel

from echo_service.web.api.endpoints.schemas.base import Attributes, DataTypes


class DataResponse(BaseModel):
    id: str
    type: DataTypes
    attributes: Attributes


class MessageResponse(BaseModel):
    data: DataResponse
