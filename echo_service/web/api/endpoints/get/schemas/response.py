from typing import List

from pydantic import BaseModel

from echo_service.web.api.endpoints.post.schemas.response import DataResponse


class MessageResponse(BaseModel):
    data: List[DataResponse]
