from model.mapping import Base
import uuid

from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship
from model.mapping.sport import SportAssociation


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = (UniqueConstraint('firstname', 'lastname'),)

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(256), nullable=False)

    sports = relationship("SportAssociation", back_populates="persons")

    def __repr__(self):
        return "<Person(%s %s)>" % (self.firstname, self.lastname.upper())

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }

    def add_sport(self, sport, level, session):
        association = SportAssociation(level=level)
        association.sports = sport
        association.person_id = self.id
        # self.sports.append(association)
        session.flush()
