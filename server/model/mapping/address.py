from model.mapping import Base
import uuid

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class Address(Base):
    __tablename__ = 'address'

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)

    street = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    postal_code = Column(Integer, nullable=False)
    country = Column(String(50), nullable=False)

    def __repr__(self):
        return "<Address (%s, %s %s, %s)>" % (self.street, self.postal_code, self.city, self.country)

    def to_dict(self):
        data = {
            "id": self.id,
            "street": self.street,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country
        }
        return data

