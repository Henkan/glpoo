import json
from flask import Blueprint, request, abort, Response

from controller.member_controller import MemberController
from model.database import DatabaseEngine
from exceptions import Error, ResourceNotFound

member_resource = Blueprint("member_resource", __name__)

# List http status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


@member_resource.route('/members', methods=['POST'])
def create_member():
    data = request.get_json()
    if data is None or len(data) == 0:
        return _error_response("Missing data", code=400)
    member_controller = _create_member_controller()
    try:
        member = member_controller.create_member(data)
        return _json_response(member, code=201)
    except Error as e:
        return _error_response(str(e), code=400)


@member_resource.route('/members', methods=['GET'])
def get_members():
    member_controller = _create_member_controller()

    try:
        # check if args in request, return all if no filter
        if "firstname" in request.args and "lastname" in request.args:
            member = member_controller.get_member_by_name(request.args.get('firstname'),
                                                          request.args.get('lastname'))
            return _json_response(member, code=200)
        else:
            members = member_controller.list_members()
            return _json_response(members, code=200)
    except Error as e:
        return _error_response(str(e), code=400)


@member_resource.route('/members/<string:member_id>', methods=['GET'])
def get_member(member_id=None):
    member_controller = _create_member_controller()
    try:
        member = member_controller.get_member(member_id)
        return _json_response(member, code=200)
    except ResourceNotFound:
        return _error_response("Member %s not found" % member_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@member_resource.route('/members/<string:member_id>', methods=['PUT'])
def update_member(member_id=None):
    member_controller = _create_member_controller()
    data = request.get_json()
    try:
        member = member_controller.update_member(member_id, data)
        return _json_response(member, code=200)
    except ResourceNotFound:
        return _error_response("Member %s not found" % member_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@member_resource.route('/members/<string:member_id>', methods=['DELETE'])
def delete_member(member_id=None):
    member_controller = _create_member_controller()
    try:
        member_controller.delete_member(member_id)
        return _json_response({}, code=204)
    except ResourceNotFound:
        return _error_response("Member %s not found" % member_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


def _json_response(data, code=200):
    return Response(json.dumps(data), content_type="application/json", status=code)


def _error_response(message, code=400):
    return _json_response({"message": message}, code=code)


def _create_member_controller():
    return MemberController(DatabaseEngine(url='sqlite:///bds.db'))
