from model.mapping import Base
import uuid
import hashlib

from sqlalchemy import Column, String, Boolean, UniqueConstraint


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (UniqueConstraint('username'),)

    id = Column(String(36), default=str(uuid.uuid4()), primary_key=True)
    username = Column(String(50), nullable=False)
    password_hash = Column(String(64))
    admin = Column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return "<User (%s, %s)>" % (self.username, self.password_hash)

    def to_dict(self):
        data = {
            "id": self.id,
            "username": self.username,
            "password_hash": self.password_hash,
            "admin": self.admin
        }
        return data

    def hash_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()
