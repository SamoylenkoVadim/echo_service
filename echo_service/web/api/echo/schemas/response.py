from pydantic import BaseModel

from echo_service.web.api.echo.schemas.request import Attributes, DataTypes


class Data(BaseModel):
    id: str
    type: DataTypes
    attributes: Attributes


class MessageResponse(BaseModel):
    data: Data
