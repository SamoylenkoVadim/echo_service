from typing import Dict, Optional

from pydantic import BaseModel, validator

from echo_service.web.api.endpoints.schemas.base import DataTypes, Methods
from echo_service.web.api.endpoints.schemas.validators import (
    validate_code,
    validate_path,
)


class Response(BaseModel):
    code: Optional[int]
    headers: Optional[Dict[str, str]]
    body: Optional[str]

    _validate_code = validator("code", allow_reuse=True)(validate_code)


class Attributes(BaseModel):
    verb: Optional[Methods]
    path: Optional[str]
    response: Optional[Response]

    _validate_path = validator("path", allow_reuse=True)(validate_path)


class DataRequest(BaseModel):
    type: DataTypes
    attributes: Attributes


class MessageRequest(BaseModel):
    data: DataRequest
