from flask_httpauth import HTTPBasicAuth
from exceptions import Error, ResourceNotFound

from controller.user_controller import UserController
from controller.person_controller import PersonController
from model.database import DatabaseEngine

auth = HTTPBasicAuth()

default_admin = {
    'username': 'admin',
    'password': 'admin'
}


@auth.verify_password
def verify_password(username, password):
    user_controller = _create_user_controller()
    if username == default_admin.get('username') and password == default_admin.get('password'):
        return {'username': 'admin', 'admin': True}
    try:
        user = user_controller.validate_credentials(username, password)
        if user is not None:
            return user

        return False
    except Error as e:
        return False


@auth.get_user_roles
def get_user_roles(user):
    user_controller = _create_user_controller()
    if user.get('username') == default_admin.get('username') and user.get('admin'):
        return 'admin'

    try:
        if user_controller.validate_admin_role(user.get('username')):
            return 'admin'
        return 'user'
    except Error as e:
        return 'user'


def check_user_has_rights(current_user, person_id):
    # Check rights so that a user can only change his information not of other members
    # Or if user is an admin
    try:
        if current_user.get('username') != 'admin':
            if current_user.get('admin'):
                return True
            connected_user = _create_person_controller().get_person_by_username(current_user.get('username'))
            if connected_user.get('id') != person_id:
                return False
    except ResourceNotFound:
        return False
    return True


def _create_user_controller():
    return UserController(DatabaseEngine(url='sqlite:///bds.db'))


def _create_person_controller():
    return PersonController(DatabaseEngine(url='sqlite:///bds.db'))
