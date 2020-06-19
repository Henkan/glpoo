from model.mapping import Base
import uuid

from sqlalchemy import Column, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship


class SportAssociation(Base):
    __tablename__ = 'sportassociation'
    __table_args__ = (UniqueConstraint('person_id', 'sport_id'),)

    person_id = Column(String(36), ForeignKey('person.id'), primary_key=True)
    sport_id = Column(String(36), ForeignKey('sport.id'), primary_key=True)
    person = relationship("Person", back_populates="sports")
    sport = relationship("Sport", back_populates="persons")
    level = Column(String(50), nullable=False)