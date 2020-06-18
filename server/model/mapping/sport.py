from model.mapping import Base
import uuid

from sqlalchemy import Column, String, UniqueConstraint


class Sport(Base):
    __tablename__ = 'sport'
    __table_args__ = (UniqueConstraint('name'),)

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(256), nullable=True)

    def __repr__(self):
        return "<Sport(%s : %s)>" % (self.name, self.description)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
