from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr


class BaseModel:
    @declared_attr
    def __tablename__(cls):  # noqa
        return cls.__name__.lower()


Model = declarative_base(cls=BaseModel)
