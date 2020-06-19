from model.mapping.person import Person

from sqlalchemy import Column, String, ForeignKey, Boolean

class Member(Person):
    __tablename__ = 'member'

    id = Column(String(36), ForeignKey('person.id'), primary_key=True)

    medical_certificate = Column(Boolean, default=False, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'member',
    }

    def __repr__(self):
        return "<Medical certificate (%s)>" % (self.medical_certificate)

    def to_dict(self):
        _dict = super().to_dict()
        _dict['medical_certificate'] = self.medical_certificate
        return _dict