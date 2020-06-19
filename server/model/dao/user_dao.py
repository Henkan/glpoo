from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from model.mapping.user import User
from model.dao.dao import DAO

from exceptions import Error, ResourceNotFound


class UserDAO(DAO):
    """
    User Mapping DAO
    """

    def __init__(self, database_session):
        super().__init__(database_session)

    def get(self, id):
        try:
            return self._database_session.query(User).filter_by(id=id).order_by(User.username).one()
        except NoResultFound:
            raise ResourceNotFound()

    def get_all(self):
        try:
            return self._database_session.query(User).order_by(User.username).all()
        except NoResultFound:
            raise ResourceNotFound()

    def get_by_name(self, username: str):
        try:
            return self._database_session.query(User).filter_by(username=username) \
                .order_by(User.username).one()
        except NoResultFound:
            raise ResourceNotFound()

    def create(self, data: dict):
        try:
            user = User(username=data.get('username'))
            user.hash_password(data.get('password'))
            self._database_session.add(user)
            self._database_session.flush()
        except IntegrityError:
            raise Error("User {0} already exists.".format(data.get('username')))
        return user

    def update(self, user: User, data: dict):
        if 'username' in data:
            user.username = data['username']
        if 'password' in data:
            user.hash_password(data['password'])
        try:
            self._database_session.merge(user)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Error data may be malformed")
        return user

    def set_role(self, user: User, role_admin: bool):
        user.admin = role_admin
        try:
            self._database_session.merge(user)
            self._database_session.flush()
        except IntegrityError:
            raise Error("Error data may be malformed")
        return user

    def delete(self, entity):
        try:
            self._database_session.delete(entity)
        except SQLAlchemyError as e:
            raise Error(str(e))
