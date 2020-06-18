import json
from flask import Blueprint, request, abort, Response

from controller.sport_controller import SportController
from model.database import DatabaseEngine
from exceptions import Error, ResourceNotFound

sport_resource = Blueprint("sport_resource", __name__)

# List http status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


@sport_resource.route('/sports', methods=['POST'])
def create_sport():
    data = request.get_json()
    if data is None or len(data) == 0:
        return _error_response("Missing data", code=400)
    sport_controller = _create_sport_controller()
    try:
        sport = sport_controller.create_sport(data)
        return _json_response(sport, code=201)
    except Error as e:
        return _error_response(str(e), code=400)


@sport_resource.route('/sports', methods=['GET'])
def get_sports():
    sport_controller = _create_sport_controller()

    try:
        # check if args in request, return all if no filter
        if "name" in request.args:
            sport = sport_controller.get_sport_by_name(request.args.get('name'))
            return _json_response(sport, code=200)
        else:
            sports = sport_controller.list_sports()
            return _json_response(sports, code=200)
    except Error as e:
        return _error_response(str(e), code=400)


@sport_resource.route('/sports/<string:sport_id>', methods=['GET'])
def get_sport(sport_id=None):
    sport_controller = _create_sport_controller()
    try:
        sport = sport_controller.get_sport(sport_id)
        return _json_response(sport, code=200)
    except ResourceNotFound:
        return _error_response("Sport %s not found" % sport_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@sport_resource.route('/sports/<string:sport_id>', methods=['PUT'])
def update_sport(sport_id=None):
    sport_controller = _create_sport_controller()
    data = request.get_json()
    try:
        sport = sport_controller.update_sport(sport_id, data)
        return _json_response(sport, code=200)
    except ResourceNotFound:
        return _error_response("Sport %s not found" % sport_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@sport_resource.route('/sports/<string:sport_id>', methods=['DELETE'])
def delete_sport(sport_id=None):
    sport_controller = _create_sport_controller()
    try:
        sport_controller.delete_sport(sport_id)
        return _json_response({}, code=204)
    except ResourceNotFound:
        return _error_response("Sport %s not found" % sport_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


def _json_response(data, code=200):
    return Response(json.dumps(data), content_type="application/json", status=code)


def _error_response(message, code=400):
    return _json_response({"message": message}, code=code)


def _create_sport_controller():
    return SportController(DatabaseEngine(url='sqlite:///bds.db'))
