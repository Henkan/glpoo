from model.mapping import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class LinkLessonMember(Base):
    __tablename__ = 'linkLessonMember'
    lesson_id = Column(
        Integer,
        ForeignKey('lesson.id'),
        primary_key=True
    )

    member_id = Column(
        Integer,
        ForeignKey('member.id'),
        primary_key=True
    )

    lesson = relationship("Lesson", back_populates="members")
    member = relationship("Member", back_populates="lessons")