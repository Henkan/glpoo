import re

from model.dao.user_dao import UserDAO
from exceptions import Error, InvalidData


class UserController:
    """
    User actions
    """

    def __init__(self, database_engine):
        self._database_engine = database_engine
        self._frames = []

    def list_users(self):
        with self._database_engine.new_session() as session:
            users = UserDAO(session).get_all()
            users_data = [user.to_dict() for user in users]
        return users_data

    def get_user(self, user_id: str):
        with self._database_engine.new_session() as session:
            user = UserDAO(session).get(user_id)
            user_data = user.to_dict()
        return user_data

    def get_user_by_name(self, name: str):
        with self._database_engine.new_session() as session:
            user = UserDAO(session).get_by_name(name)
            user_data = user.to_dict()
        return user_data

    def create_user(self, data):
        self._check_profile_data(data)
        try:
            with self._database_engine.new_session() as session:
                user = UserDAO(session).create(data)
                user_data = user.to_dict()
                return user_data
        except Error as e:
            # log error
            raise e

    def update_user(self, user_id: str, user_data: dict):
        self._check_profile_data(user_data, update=True)
        with self._database_engine.new_session() as session:
            user_dao = UserDAO(session)
            user = user_dao.get(user_id)
            user = user_dao.update(user, user_data)
            return user.to_dict()

    def set_user_role(self, user_id: str, admin: bool):
        with self._database_engine.new_session() as session:
            user_dao = UserDAO(session)
            user = user_dao.get(user_id)
            user = user_dao.set_role(user, admin)
            return user.to_dict()

    def delete_user(self, user_id: str):
        with self._database_engine.new_session() as session:
            user_dao = UserDAO(session)
            user = user_dao.get(user_id)
            user_dao.delete(user)

    def search_user(self, name: str):
        # Query database
        with self._database_engine.new_session() as session:
            user_dao = UserDAO(session)
            user = user_dao.get_by_name(name)
            return user.to_dict()

    def validate_credentials(self, username: str, password: str):
        with self._database_engine.new_session() as session:
            user_dao = UserDAO(session)
            user = user_dao.get_by_name(username)
            return user.check_password(password)

    def validate_admin_role(self, username: str):
        with self._database_engine.new_session() as session:
            user_dao = UserDAO(session)
            user = user_dao.get_by_name(username)
            return user.admin

    def _check_profile_data(self, data, update=False):
        mandatories = {
            'username': {"type": str},
            'password': {"type": str}
        }
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
