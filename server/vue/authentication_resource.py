from flask_httpauth import HTTPBasicAuth
from exceptions import Error, ResourceNotFound

from controller.user_controller import UserController
from model.database import DatabaseEngine

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user_controller = _create_user_controller()
    try:
        return user_controller.validate_credentials(username, password)
    except Error as e:
        return False


# TODO: roles: user, admin, user=person
@auth.get_user_roles
def get_user_roles(user):
    user_controller = _create_user_controller()
    try:
        if user_controller.validate_admin_role(user.get('username')):
            return 'admin'
        return 'user'
    except Error as e:
        return 'user'


def _create_user_controller():
    return UserController(DatabaseEngine(url='sqlite:///bds.db'))
