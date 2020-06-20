from model.mapping import Base, generate_id
from model.mapping.linkLessonMember import LinkLessonMember
import uuid

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship



class Lesson(Base):
    __tablename__ = 'lesson'

    id = Column(String(36), default=generate_id, primary_key=True)
    date = Column(String(20), nullable=False)
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    level = Column(String(50), nullable=False)
    members = relationship('LinkLessonMember', back_populates = 'lesson')

    def __repr__(self):
        return "<Lesson on %s : %s - %s . Level : %s>" % (self.date, self.start_time, self.end_time, self.level)

    def to_dict(self):
        data = {
            "id":self.id,
            "date":self.date,
            "start_time":self.start_time,
            "end_time":self.end_time,
            "level":self.level
        }
        return data
