from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from model.mapping.lesson import Lesson
from model.mapping.coach import Coach
from model.dao.dao import DAO

from exceptions import Error, ResourceNotFound


class LessonDAO(DAO):
    """
    Lesson Mapping DAO
    """

    def __init__(self, database_session):
        super().__init__(database_session)

    def get(self, id):
        try:
            return self._database_session.query(Lesson).filter_by(id=id).order_by(Lesson.date).one()
        except NoResultFound:
            raise ResourceNotFound()

    def get_all(self):
        try:
            return self._database_session.query(Lesson).order_by(Lesson.date).all()
        except NoResultFound:
            raise ResourceNotFound()

    def get_by_date_time(self, date: str, start_time: int, end_time: int):
        try:
            return self._database_session.query(Lesson).filter_by(date=date, start_time=start_time, end_time=end_time) \
                .order_by(Lesson.date).one()
        except NoResultFound:
            raise ResourceNotFound()

    def create(self, data: dict):
        try:
            lesson = Lesson(date=data.get('date'), start_time=data.get('start_time'), end_time=data.get('end_time'),
                            level=data.get('level'))

            self._database_session.add(lesson)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Lesson already exists")
        return lesson

    def update(self, lesson: Lesson, data: dict):
        if 'date' in data:
            lesson.date = data['date']
        if 'start_time' in data:
            lesson.start_time = data['start_time']
        if 'end_time' in data:
            lesson.end_time = data['end_time']
        if 'level' in data:
            lesson.level = data['level']

        try:
            self._database_session.merge(lesson)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Error data may be malformed")
        return lesson

    def delete(self, entity: Lesson):
        try:
            self._database_session.delete(entity)
        except SQLAlchemyError as e:
            raise Error(str(e))

    def add_coach(self, lesson: Lesson, coach: Coach, session):
        lesson.coach_id = coach.id
        coach.lessons.append(lesson)
        session.flush()

    def delete_coach(self, lesson: Lesson, coach: Coach, session):
        for link_lesson in coach.lessons:
            if link_lesson == lesson:
                coach.lessons.remove(link_lesson)
                lesson.coach_id = None
                session.flush()
                break