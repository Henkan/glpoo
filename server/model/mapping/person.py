from model.mapping import Base
import uuid

from sqlalchemy import Column, String, UniqueConstraint


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = (UniqueConstraint('firstname', 'lastname'),)

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    person_type = Column(String(50), nullable=False)

    email = Column(String(256), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': person_type
    }

    def __repr__(self):
        return "<Person(%s %s)>" % (self.firstname, self.lastname.upper())

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }
