import re

from model.dao.lesson_dao import LessonDAO
from model.dao.coach_dao import CoachDAO
from exceptions import Error, InvalidData


class LessonController:
    """
    Lesson actions
    """

    def __init__(self, database_engine):
        self._database_engine = database_engine
        self._frames = []

    def list_lessons(self):
        with self._database_engine.new_session() as session:
            lessons = LessonDAO(session).get_all()
            lessons_data = [lesson.to_dict() for lesson in lessons]
        return lessons_data

    def get_lesson(self, lesson_id: str):
        with self._database_engine.new_session() as session:
            lesson = LessonDAO(session).get(lesson_id)
            lesson_data = lesson.to_dict()
        return lesson_data

    def get_lesson_by_date_time(self, date: str, start_time: int, end_time: int):
        with self._database_engine.new_session() as session:
            lesson = LessonDAO(session).get_by_date_time(date, start_time, end_time)
            lesson_data = lesson.to_dict()
        return lesson_data

    def create_lesson(self, data: dict):
        self._check_profile_data(data)
        try:
            with self._database_engine.new_session() as session:
                # Save lesson in database
                lesson = LessonDAO(session).create(data)
                lesson_data = lesson.to_dict()
                return lesson_data
        except Error as e:
            # log error
            raise e

    def update_lesson(self, lesson_id: str, lesson_data: dict):
        self._check_profile_data(lesson_data, update=True)
        with self._database_engine.new_session() as session:
            lesson_dao = LessonDAO(session)
            lesson = lesson_dao.get(lesson_id)
            lesson = lesson_dao.update(lesson, lesson_data)
            return lesson.to_dict()

    def delete_lesson(self, lesson_id: str):
        with self._database_engine.new_session() as session:
            lesson_dao = LessonDAO(session)
            lesson = lesson_dao.get(lesson_id)
            lesson_dao.delete(lesson)

    def search_lesson(self, date: str, start_time: int, end_time: int):
        # Query database
        with self._database_engine.new_session() as session:
            lesson_dao = LessonDAO(session)
            lesson = lesson_dao.get_by_date_time(date, start_time, end_time)
            return lesson.to_dict()

    def add_coach_lesson(self, lesson_id: str, coach_id: str):
        with self._database_engine.new_session() as session:
            lesson_dao = LessonDAO(session)
            lesson = lesson_dao.get(lesson_id)
            coach_dao = CoachDAO(session)
            coach = coach_dao.get(coach_id)
            lesson_dao.add_coach(lesson, coach, session)

    def delete_coach_lesson(self, lesson_id: str, coach_id: str):
        with self._database_engine.new_session() as session:
            lesson_dao = LessonDAO(session)
            lesson = lesson_dao.get(lesson_id)
            coach_dao = CoachDAO(session)
            coach = coach_dao.get(coach_id)
            lesson_dao.delete_coach(lesson, coach, session)

    def _check_profile_data(self, data: dict, update=False):
        mandatories = {
            'date': {"type": str},
            'start_time': {"type": int},
            'end_time': {"type": int},
            'level': {"type": str}
        }

        if (('start_time' in data == True) and ('end_time' in data == True)):
            if data['start_time'] > data['end_time']:
                raise InvalidData("End time must be superior than start time")

        for mandatory, specs in mandatories.items():
            if not update:
                if mandatory not in data or data[mandatory] is None:
                    raise InvalidData("Missing value %s" % mandatory)
            else:
                if mandatory not in data:
                    continue
            value = data[mandatory]
            if "type" in specs and not isinstance(value, specs["type"]):
                raise InvalidData("Invalid type %s" % mandatory)