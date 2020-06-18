import re

from model.dao.coach_dao import CoachDAO
from exceptions import Error, InvalidData


class CoachController:
    """
    Coach actions
    """

    def __init__(self, database_engine):
        self._database_engine = database_engine
        self._frames = []

    def list_coachs(self):
        with self._database_engine.new_session() as session:
            coachs = CoachDAO(session).get_all()
            coachs_data = [coach.to_dict() for coach in coachs]
        return coachs_data

    def get_coach(self, coach_id: str):
        with self._database_engine.new_session() as session:
            coach = CoachDAO(session).get(coach_id)
            coach_data = coach.to_dict()
        return coach_data

    def get_coach_by_name(self, firstname: str, lastname: str):
        with self._database_engine.new_session() as session:
            coach = CoachDAO(session).get_by_name(firstname, lastname)
            coach_data = coach.to_dict()
        return coach_data

    def create_coach(self, data: dict):
        self._check_profile_data(data)
        try:
            with self._database_engine.new_session() as session:
                # Save sport in database
                coach = CoachDAO(session).create(data)
                coach_data = coach.to_dict()
                return coach_data
        except Error as e:
            # log error
            raise e

    def update_coach(self, coach_id: str, coach_data: dict):
        self._check_profile_data(coach_data, update=True)
        with self._database_engine.new_session() as session:
            coach_dao = CoachDAO(session)
            coach = coach_dao.get(coach_id)
            coach = coach_dao.update(coach, coach_data)
            return coach.to_dict()

    def delete_coach(self, coach_id: str):
        with self._database_engine.new_session() as session:
            coach_dao = CoachDAO(session)
            coach = coach_dao.get(coach_id)
            coach_dao.delete(coach)

    def search_coach(self, firstname: str, lastname: str):
        # Query database
        with self._database_engine.new_session() as session:
            coach_dao = CoachDAO(session)
            coach = coach_dao.get_by_name(firstname, lastname)
            return coach.to_dict()

    def _check_profile_data(self, data: dict, update=False):
        name_pattern = re.compile("^[\S-]{2,50}$")
        email_pattern = re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
        mandatories = {
            'firstname': {"type": str, "regex": name_pattern},
            'lastname': {"type": str, "regex": name_pattern},
            'email': {"type": str, "regex": email_pattern},
            'degree': {"type": str, "regex": name_pattern}
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
            if "regex" in specs and isinstance(value, str) and not re.match(specs["regex"], value):
                raise InvalidData("Invalid value %s" % mandatory)