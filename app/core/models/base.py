from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr

from core.config import settings


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.convention,
    )

    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"
