from model.mapping import Base, generate_id
from model.mapping.link_lesson_member import LinkLessonMember
import uuid

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(String(36), default=generate_id, primary_key=True)
    date = Column(String(20), nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    level = Column(String(50), nullable=False)

    coach_id = Column(String(36), ForeignKey('coach.id'))
    sport_id = Column(String(36), ForeignKey('sport.id'))
    coach = relationship("Coach", back_populates="lessons")
    sport = relationship("Sport", back_populates="lessons")
    members = relationship('LinkLessonMember', back_populates='lesson')

    def __repr__(self):
        return "<Lesson on %s : %s - %s . Level : %s>" % (self.date, self.start_time, self.end_time, self.level)

    def to_dict(self):
        data = {
            "id": self.id,
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "level": self.level,
            "coach": self.coach_id,
            "sport": self.sport_id
        }
        return data
