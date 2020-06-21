from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from model.mapping.member import Member
from model.dao.dao import DAO
from model.mapping.lesson import Lesson
from model.mapping.link_lesson_member import LinkLessonMember

from exceptions import Error, ResourceNotFound


class MemberDAO(DAO):
    """
    Member Mapping DAO
    """

    def __init__(self, database_session):
        super().__init__(database_session)

    def get(self, id: str):
        try:
            return self._database_session.query(Member).filter_by(id=id).order_by(Member.firstname).one()
        except NoResultFound:
            print('here')
            raise ResourceNotFound()

    def get_all(self):
        try:
            return self._database_session.query(Member).order_by(Member.firstname).all()
        except NoResultFound:
            raise ResourceNotFound()

    def get_by_name(self, firstname: str, lastname: str):
        try:
            return self._database_session.query(Member).filter_by(firstname=firstname, lastname=lastname) \
                .order_by(Member.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def create(self, data: dict):
        try:
            member = Member(firstname=data.get('firstname'), lastname=data.get('lastname'), email=data.get('email'),
                          medical_certificate=data.get('medical_certificate'))
            self._database_session.add(member)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Member already exists.")
        return member

    def update(self, member: Member, data: dict):
        if 'firstname' in data:
            member.firstname = data['firstname']
        if 'lastname' in data:
            member.lastname = data['lastname']
        if 'email' in data:
            member.email = data['email']
        if 'medical_certificate' in data:
            member.medical_certificate = data['medical_certificate']
        try:
            self._database_session.merge(member)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Error data may be malformed")
        return member

    def delete(self, entity: Member):
        try:
            self._database_session.delete(entity)
        except SQLAlchemyError as e:
            raise Error(str(e))

    def add_lesson(self, member: Member, lesson: Lesson, session):
        link = LinkLessonMember()
        link.lesson = lesson
        link.member_id = member.id
        session.flush()

    def delete_lesson(self, member: Member, lesson: Lesson, session):
        for link in member.lessons:
            if link == lesson:
                member.lessons.remove(link)
                session.delete(link)
                session.flush()
                break
