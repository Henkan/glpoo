from model.mapping import Base
import uuid

from sqlalchemy import Column, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship
from model.mapping.sport import SportAssociation


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = (UniqueConstraint('firstname', 'lastname'),)

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(256), nullable=False)

    sports = relationship("SportAssociation", back_populates="person")

    address_id = Column(String(36), ForeignKey('address.id'), nullable=True)

    address = relationship('Address')

    def __repr__(self):
        return "<Person(%s %s)>" % (self.firstname, self.lastname.upper())

    def to_dict(self):
        data = {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "sports": []
        }
        for association in self.sports:
            data.get("sports").append({"name": association.sport.name, "level": association.level})
        if self.address is not None:
            data['address'] = self.address.to_dict()
        return data

    def add_sport(self, sport, level, session):
        association = SportAssociation(level=level)
        association.sport = sport
        association.person_id = self.id
        session.flush()

    def delete_sport(self, sport, session):
        for association in self.sports:
            if association.sport == sport:
                self.sports.remove(association)
                session.delete(association)
                session.flush()
                break
