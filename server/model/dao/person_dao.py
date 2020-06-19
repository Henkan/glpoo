from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from model.mapping.person import Person
from model.mapping.user import User
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
            return self._database_session.query(Person).filter_by(firstname=firstname, lastname=lastname) \
                .order_by(Person.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def get_by_id_user(self, id_user: str):
        try:
            return self._database_session.query(Person).filter_by(user_id=id_user).order_by(Person.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def create(self, data: dict):
        try:
            person = Person(firstname=data.get('firstname'), lastname=data.get('lastname'), email=data.get('email'))

            if 'address' in data.keys():
                tmp = data.get('address')
                person.set_address(street=tmp.get('street'), postal_code=tmp.get('postal_code'),
                                   country=tmp.get('country'), city=tmp.get('city'))

            if 'user' in data.keys():
                usr = data.get('user')
                person.set_user(username=usr.get('username'), password=usr.get('password'), admin=usr.get('admin'))

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
        if 'address' in data:
            if 'street' in data['address']:
                person.address.street = data['address']['street']
            if 'postal_code' in data['address']:
                person.address.postal_code = data['address']['postal_code']
            if 'city' in data['address']:
                person.address.city = data['address']['city']
            if 'country' in data['address']:
                person.address.country = data['address']['country']
        if 'user' in data:
            if 'username' in data['user']:
                person.user.username = data['user']['username']
            if 'password' in data['user']:
                person.user.hash_password(data['user']['password'])

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
