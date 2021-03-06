import json
from flask import Blueprint, request, abort, Response

from controller.lesson_controller import LessonController
from model.database import DatabaseEngine
from exceptions import Error, ResourceNotFound

from vue.authentication_resource import auth, check_user_has_rights

lesson_resource = Blueprint("lesson_resource", __name__)


# List http status codes: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes


@lesson_resource.route('/lesson', methods=['POST'])
@auth.login_required(role='admin')
def create_lesson():
    data = request.get_json()
    if data is None or len(data) == 0:
        return _error_response("Missing data", code=400)
    lesson_controller = _create_lesson_controller()
    try:
        lesson = lesson_controller.create_lesson(data)
        return _json_response(lesson, code=201)
    except Error as e:
        return _error_response(str(e), code=400)


@lesson_resource.route('/lessons', methods=['GET'])
def get_lessons():
    lesson_controller = _create_lesson_controller()

    try:
        # check if args in request, return all if no filter
        if "date" in request.args and "start_time" in request.args and "end_time" in request.args:
            lesson = lesson_controller.get_lesson_by_date_time(request.args.get('date'),
                                                        request.args.get('start_time'),
                                                        request.args.get('end_time'))
            return _json_response(lesson, code=200)
        else:
            lessons = lesson_controller.list_lessons()
            return _json_response(lessons, code=200)
    except Error as e:
        return _error_response(str(e), code=400)


@lesson_resource.route('/lesson/<string:lesson_id>', methods=['GET'])
def get_lesson(lesson_id=None):
    lesson_controller = _create_lesson_controller()
    try:
        lesson = lesson_controller.get_lesson(lesson_id)
        return _json_response(lesson, code=200)
    except ResourceNotFound:
        return _error_response("Lesson %s not found" % lesson_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@lesson_resource.route('/lesson/<string:lesson_id>', methods=['PUT'])
@auth.login_required(role='admin')
def update_lesson(lesson_id=None):
    lesson_controller = _create_lesson_controller()
    data = request.get_json()
    try:
        lesson = lesson_controller.update_lesson(lesson_id, data)
        return _json_response(lesson, code=200)
    except ResourceNotFound:
        return _error_response("Lesson %s not found" % lesson_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@lesson_resource.route('/lesson/<string:lesson_id>', methods=['DELETE'])
@auth.login_required(role='admin')
def delete_lesson(lesson_id=None):
    lesson_controller = _create_lesson_controller()
    try:
        lesson_controller.delete_lesson(lesson_id)
        return _json_response({}, code=204)
    except ResourceNotFound:
        return _error_response("Lesson %s not found" % lesson_id, code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@lesson_resource.route('/lesson/<string:lesson_id>/coach/<string:coach_id>', methods=['PUT'])
@auth.login_required(role='admin')
def add_coach_lesson(lesson_id=None, coach_id=None):
    lesson_controller = _create_lesson_controller()
    try:
        lesson_controller.add_coach_lesson(lesson_id, coach_id)
        return _json_response('coach added', code=200)
    except ResourceNotFound:
        return _error_response("Coach cannot be add", code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@lesson_resource.route('/lesson/<string:lesson_id>/coach/<string:coach_id>', methods=['DELETE'])
@auth.login_required(role='admin')
def delete_coach_lesson(lesson_id=None, coach_id=None):
    lesson_controller = _create_lesson_controller()
    try:
        lesson_controller.delete_coach_lesson(lesson_id, coach_id)
        return _json_response('coach delete', code=204)
    except ResourceNotFound:
        return _error_response("Coach is not deleted", code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@lesson_resource.route('/lesson/<string:lesson_id>/sport/<string:sport_id>', methods=['PUT'])
@auth.login_required(role='admin')
def add_sport_lesson(lesson_id=None, sport_id=None):
    lesson_controller = _create_lesson_controller()
    try:
        lesson_controller.add_sport_lesson(lesson_id, sport_id)
        return _json_response('sport added', code=200)
    except ResourceNotFound:
        return _error_response("sport cannot be add", code=404)
    except Error as e:
        return _error_response(str(e), code=400)


@lesson_resource.route('/lesson/<string:lesson_id>/sport/<string:sport_id>', methods=['DELETE'])
@auth.login_required(role='admin')
def delete_sport_lesson(lesson_id=None, sport_id=None):
    lesson_controller = _create_lesson_controller()
    try:
        lesson_controller.delete_sport_lesson(lesson_id, sport_id)
        return _json_response('sport delete', code=204)
    except ResourceNotFound:
        return _error_response("sport is not deleted", code=404)
    except Error as e:
        return _error_response(str(e), code=400)


def _json_response(data, code=200):
    return Response(json.dumps(data), content_type="application/json", status=code)


def _error_response(message, code=400):
    return _json_response({"message": message}, code=code)


def _create_lesson_controller():
    return LessonController(DatabaseEngine(url='sqlite:///bds.db'))
