from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class Base:
  @declared_attr
  def __tablename__(cls):
    return cls.__name__.lower()

  def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}
