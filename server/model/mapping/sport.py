from model.mapping import Base
import uuid

from sqlalchemy import Column, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship


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

    def add_person(self, person, level, session):
        association = SportAssociation(level=level)
        association.sport_id = self.id
        association.persons = person
        # self.sports.append(association)
        session.flush()


class SportAssociation(Base):
    __tablename__ = 'sportassociation'
    __table_args__ = (UniqueConstraint('person_id', 'sport_id'),)

    person_id = Column(String(36), ForeignKey('person.id'), primary_key=True)
    sport_id = Column(String(36), ForeignKey('sport.id'), primary_key=True)
    persons = relationship("Person", back_populates="sports")
    sports = relationship("Sport", back_populates="persons")
    level = Column(String(50), nullable=False)
