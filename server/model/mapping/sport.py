from model.mapping import Base
import uuid

from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship

from model.mapping.sport_association import SportAssociation


class Sport(Base):
    __tablename__ = 'sport'
    __table_args__ = (UniqueConstraint('name'),)

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(256), nullable=True)

    persons = relationship("SportAssociation", back_populates="sport")

    def __repr__(self):
        return "<Sport(%s : %s)>" % (self.name, self.description)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
