from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from model.mapping.person import Person
from model.dao.dao import DAO

from exceptions import Error, ResourceNotFound


class PersonDAO(DAO):
    """
    Person Mapping DAO
    """

    def __init__(self, database_session):
        super().__init__(database_session)

    def get(self, id):
        try:
            return self._database_session.query(Person).filter_by(id=id).order_by(Person.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def get_all(self):
        try:
            return self._database_session.query(Person).order_by(Person.firstname).all()
        except NoResultFound:
            raise ResourceNotFound()

    def get_by_name(self, firstname: str, lastname: str):
        try:
            return self._database_session.query(Person).filter_by(firstname=firstname, lastname=lastname)\
                .order_by(Person.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def create(self, data: dict):
        try:
            person = Person(firstname=data.get('firstname'), lastname=data.get('lastname'), email=data.get('email'))
            self._database_session.add(person)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Person already exists")
        return person

    def update(self, person: Person, data: dict):
        if 'firstname' in data:
            person.firstname = data['firstname']
        if 'lastname' in data:
            person.lastname = data['lastname']
        if 'email' in data:
            person.email = data['email']
        try:
            self._database_session.merge(person)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Error data may be malformed")
        return person

    def delete(self, entity):
        try:
            self._database_session.delete(entity)
        except SQLAlchemyError as e:
            raise Error(str(e))
