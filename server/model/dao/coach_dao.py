from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from model.mapping.coach import Coach
from model.dao.dao import DAO

from exceptions import Error, ResourceNotFound


class CoachDAO(DAO):
    """
    Coach Mapping DAO
    """

    def __init__(self, database_session):
        super().__init__(database_session)

    def get(self, id: str):
        try:
            return self._database_session.query(Coach).filter_by(id=id).order_by(Coach.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def get_all(self):
        try:
            return self._database_session.query(Coach).order_by(Coach.firstname).all()
        except NoResultFound:
            raise ResourceNotFound()

    def get_by_name(self, firstname: str, lastname: str):
        try:
            return self._database_session.query(Coach).filter_by(firstname=firstname, lastname=lastname) \
                .order_by(Coach.firstname).one()
        except NoResultFound:
            raise ResourceNotFound()

    def create(self, data: dict):
        try:
            coach = Coach(firstname=data.get('firstname'), lastname=data.get('lastname'), email=data.get('email'),
                          contract=data.get('contract'), degree=data.get('degree'))
            self._database_session.add(coach)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Coach already exists.")
        return coach

    def update(self, coach: Coach, data: dict):
        if 'firstname' in data:
            coach.firstname = data['firstname']
        if 'lastname' in data:
            coach.lastname = data['lastname']
        if 'email' in data:
            coach.email = data['email']
        if 'contract' in data:
            coach.contract = data['contract']
        if 'degree' in data:
            coach.degree = data['degree']
        try:
            self._database_session.merge(coach)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Error data may be malformed")
        return coach

    def delete(self, entity: Coach):
        try:
            self._database_session.delete(entity)
        except SQLAlchemyError as e:
            raise Error(str(e))
