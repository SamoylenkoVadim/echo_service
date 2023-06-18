import re
from enum import Enum
from typing import Dict, Optional

from pydantic import BaseModel, validator


class DataTypes(Enum):
    endpoints = "endpoints"


class Methods(Enum):
    get = "GET"
    post = "POST"
    put = "PUT"
    patch = "PATCH"
    delete = "DELETE"


class Response(BaseModel):
    code: int
    headers: Optional[Dict[str, str]]
    body: Optional[str]

    @validator("code")
    def validate_code(cls, code: int) -> int:
        if code < 100 or code > 599:
            raise ValueError("Invalid HTTP code. Must be between 100 and 599.")
        return code


class Attributes(BaseModel):
    verb: Methods
    path: str
    response: Response

    @validator("path")
    def validate_path(cls, path: str) -> str:
        pattern = "^/[a-zA-Z0-9_/]+$"
        if not re.match(pattern, path):
            raise ValueError(
                "Invalid URL path format. path_pattern: ^/[a-zA-Z0-9_/]+$",
            )

        return path


class Data(BaseModel):
    type: DataTypes
    attributes: Attributes


class Request(BaseModel):
    data: Data
