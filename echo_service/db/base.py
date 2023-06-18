from sqlalchemy.orm import DeclarativeBase

from echo_service.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
