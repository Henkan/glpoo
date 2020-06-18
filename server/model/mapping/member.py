from model.mapping import Base
import uuid

from sqlalchemy import Column, String, UniqueConstraint


class Member(Base):
    __tablename__ = 'members'
    __table_args__ = (UniqueConstraint('firstname', 'lastname'),)

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)

    email = Column(String(256), nullable=False)

    def __repr__(self):
        return "<Member(%s %s)>" % (self.firstname, self.lastname.upper())

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
        }
