import json
from flask import Blueprint, request, Response

from controller.user_controller import UserController
from model.database import DatabaseEngine
from exceptions import Error, ResourceNotFound

from vue.authentication_resource import auth

user_resource = Blueprint("user_resource", __name__)


@user_resource.route('/users', methods=['POST'])
@auth.login_required(role='admin')
def create_user():
    data = request.get_json()
    if data is None or len(data) == 0:
        return _error_response("Missing data", code=400)
    user_controller = _create_user_controller()
    try:
        user = user_controller.create_user(data)
        return _json_response(user, code=201)
    except Error as e:
        return _error_response(str(e), code=400)


@user_resource.route('/users/<string:user_id>', methods=['POST'])
@auth.login_required(role='admin')
def set_user_role(user_id=None):
    # Set a user as admin
    user_controller = _create_user_controller()
    data = request.get_json()
    if data is None or len(data) == 0:
        return _error_response("Missing data", code=400)
    try:
        user = user_controller.set_user_role(user_id, data.get("admin"))
        return _json_response(user, code=200)
    except ResourceNotFound:
        return _error_response("User %s not found" % user_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@user_resource.route('/users', methods=['GET'])
@auth.login_required()
def get_users():
    user_controller = _create_user_controller()
    try:
        # check if args in request, return all if no filter
        if "username" in request.args:
            user = user_controller.get_user_by_name(request.args.get('name'))
            return _json_response(user, code=200)
        else:
            users = user_controller.list_users()
            return _json_response(users, code=200)
    except Error as e:
        return _error_response(str(e), code=400)


@user_resource.route('/users/<string:user_id>', methods=['GET'])
@auth.login_required()
def get_user(user_id=None):
    user_controller = _create_user_controller()
    try:
        user = user_controller.get_user(user_id)
        return _json_response(user, code=200)
    except ResourceNotFound:
        return _error_response("User %s not found" % user_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@user_resource.route('/users/<string:user_id>', methods=['PUT'])
def update_user(user_id=None):
    user_controller = _create_user_controller()
    data = request.get_json()
    try:
        user = user_controller.update_user(user_id, data)
        return _json_response(user, code=200)
    except ResourceNotFound:
        return _error_response("User %s not found" % user_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@user_resource.route('/users/<string:user_id>', methods=['DELETE'])
def delete_user(user_id=None):
    user_controller = _create_user_controller()
    try:
        user_controller.delete_user(user_id)
        return _json_response({}, code=204)
    except ResourceNotFound:
        return _error_response("User %s not found" % user_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


def _json_response(data, code=200):
    return Response(json.dumps(data), content_type="application/json", status=code)


def _error_response(message, code=400):
    return _json_response({"message": message}, code=code)


def _create_user_controller():
    return UserController(DatabaseEngine(url='sqlite:///bds.db'))
