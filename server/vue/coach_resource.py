import json
from flask import Blueprint, request, abort, Response

from controller.coach_controller import CoachController
from model.database import DatabaseEngine
from exceptions import Error, ResourceNotFound

coach_resource = Blueprint("coach_resource", __name__)


# List http status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


@coach_resource.route('/coach', methods=['POST'])
def create_coach():
    data = request.get_json()
    if data is None or len(data) == 0:
        return _error_response("Missing data", code=400)
    coach_controller = _create_coach_controller()
    try:
        coach = coach_controller.create_coach(data)
        return _json_response(coach, code=201)
    except Error as e:
        return _error_response(str(e), code=400)


@coach_resource.route('/coachs', methods=['GET'])
def get_coachs():
    coach_controller = _create_coach_controller()

    try:
        # check if args in request, return all if no filter
        if "firstname" in request.args and "lastname" in request.args:
            coach = coach_controller.get_person_by_name(request.args.get('firstname'),
                                                        request.args.get('lastname'))
            return _json_response(coach, code=200)
        else:
            coachs = coach_controller.list_coachs()
            return _json_response(coachs, code=200)
    except Error as e:
        return _error_response(str(e), code=400)


@coach_resource.route('/coach/<string:coach_id>', methods=['GET'])
def get_coach(coach_id=None):
    coach_controller = _create_coach_controller()
    try:
        coach = coach_controller.get_coach(coach_id)
        return _json_response(coach, code=200)
    except ResourceNotFound:
        return _error_response("Coach %s not found" % coach_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@coach_resource.route('/coach/<string:coach_id>', methods=['PUT'])
def update_coach(coach_id=None):
    coach_controller = _create_coach_controller()
    data = request.get_json()
    try:
        coach = coach_controller.update_coach(coach_id, data)
        return _json_response(coach, code=200)
    except ResourceNotFound:
        return _error_response("Coach %s not found" % coach_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@coach_resource.route('/coach/<string:coach_id>', methods=['DELETE'])
def delete_person(coach_id=None):
    coach_controller = _create_coach_controller()
    try:
        coach_controller.delete_coach(coach_id)
        return _json_response({}, code=204)
    except ResourceNotFound:
        return _error_response("Coach %s not found" % coach_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


def _json_response(data, code=200):
    return Response(json.dumps(data), content_type="application/json", status=code)


def _error_response(message, code=400):
    return _json_response({"message": message}, code=code)


def _create_coach_controller():
    return CoachController(DatabaseEngine(url='sqlite:///bds.db'))
