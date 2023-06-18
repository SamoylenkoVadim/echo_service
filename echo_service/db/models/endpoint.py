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
