import json
from flask import Blueprint, request, abort, Response

from controller.person_controller import PersonController
from model.database import DatabaseEngine
from exceptions import Error, ResourceNotFound

person_resource = Blueprint("person_resource", __name__)

# List http status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


@person_resource.route('/persons', methods=['POST'])
def create_person():
    data = request.get_json()
    if data is None or len(data) == 0:
        return _error_response("Missing data", code=400)
    person_controller = _create_person_controller()
    try:
        person = person_controller.create_person(data)
        return _json_response(person, code=201)
    except Error as e:
        return _error_response(str(e), code=400)


@person_resource.route('/persons', methods=['GET'])
def get_persons():
    person_controller = _create_person_controller()

    try:
        # check if args in request, return all if no filter
        if "firstname" in request.args and "lastname" in request.args:
            person = person_controller.get_person_by_name(request.args.get('firstname'),
                                                          request.args.get('lastname'))
            return _json_response(person, code=200)
        else:
            persons = person_controller.list_persons()
            return _json_response(persons, code=200)
    except Error as e:
        return _error_response(str(e), code=400)


@person_resource.route('/persons/<string:person_id>', methods=['GET'])
def get_person(person_id=None):
    person_controller = _create_person_controller()
    try:
        person = person_controller.get_person(person_id)
        return _json_response(person, code=200)
    except ResourceNotFound:
        return _error_response("Person %s not found" % person_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@person_resource.route('/persons/<string:person_id>', methods=['PUT'])
def update_person(person_id=None):
    person_controller = _create_person_controller()
    data = request.get_json()
    try:
        person = person_controller.update_person(person_id, data)
        return _json_response(person, code=200)
    except ResourceNotFound:
        return _error_response("Person %s not found" % person_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@person_resource.route('/persons/<string:person_id>', methods=['DELETE'])
def delete_person(person_id=None):
    person_controller = _create_person_controller()
    try:
        person_controller.delete_person(person_id)
        return _json_response({}, code=204)
    except ResourceNotFound:
        return _error_response("Person %s not found" % person_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


def _json_response(data, code=200):
    return Response(json.dumps(data), content_type="application/json", status=code)


def _error_response(message, code=400):
    return _json_response({"message": message}, code=code)


def _create_person_controller():
    return PersonController(DatabaseEngine(url='sqlite:///bds.db'))
