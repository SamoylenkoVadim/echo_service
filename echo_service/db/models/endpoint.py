from typing import Dict

from sqlalchemy import JSON, Column, Integer, String

from echo_service.db.base import Base


class Endpoint(Base):
    __tablename__ = "endpoints"

    id = Column(Integer, primary_key=True, index=True)
    verb = Column(String, index=True)
    path = Column(String, index=True)
    response_code = Column(Integer)
    response_headers = Column(JSON)
    response_body = Column(String)

    def __repr__(self) -> str:
        return f"<Endpoint id={self.id}, " f"verb={self.verb}, " f"path={self.path}>"

    @property
    def get_id(self) -> int:
        return int(self.id)

    @property
    def get_path(self) -> str:
        return str(self.path)

    @property
    def get_verb(self) -> str:
        return str(self.verb)

    @property
    def get_body(self) -> str:
        return str(self.response_body)

    @property
    def get_headers(self) -> Dict[str, str]:
        return self.response_headers  # type: ignore

    @property
    def get_code(self) -> int:
        return int(self.response_code)
