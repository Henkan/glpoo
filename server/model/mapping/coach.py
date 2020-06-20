from model.mapping.person import Person

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

class Coach(Person):
    __tablename__ = 'coach'

    id = Column(String(36), ForeignKey('person.id'), primary_key=True)

    contract = Column(String(50), nullable=False)
    degree = Column(String(50), nullable=False)

    lessons = relationship("Lesson", back_populates="coach")

    __mapper_args__ = {
        'polymorphic_identity': 'coach',
    }

    def __repr__(self):
        return "<Coach(%s %s)>" % (self.contract, self.degree)

    def to_dict(self):
        _dict = super().to_dict()
        _dict['contract'] = self.contract
        _dict['degree'] = self.degree
        _dict['lessons'] = []

        for link in self.lessons:
            _dict['lessons'].append({"date": link.date})

        return _dict
