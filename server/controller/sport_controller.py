import re

from model.dao.sport_dao import SportDAO
from exceptions import Error, InvalidData


class SportController:
    """
    Sport actions
    """

    def __init__(self, database_engine):
        self._database_engine = database_engine
        self._frames = []

    def list_sports(self):
        with self._database_engine.new_session() as session:
            sports = SportDAO(session).get_all()
            sports_data = [sport.to_dict() for sport in sports]
        return sports_data

    def get_sport(self, sport_id: str):
        with self._database_engine.new_session() as session:
            sport = SportDAO(session).get(sport_id)
            sport_data = sport.to_dict()
        return sport_data

    def get_sport_by_name(self, name: str):
        with self._database_engine.new_session() as session:
            sport = SportDAO(session).get_by_name(name)
            sport_data = sport.to_dict()
        return sport_data

    def create_sport(self, data):
        self._check_profile_data(data)
        try:
            with self._database_engine.new_session() as session:
                # Save sport in database
                sport = SportDAO(session).create(data)
                sport_data = sport.to_dict()
                return sport_data
        except Error as e:
            # log error
            raise e

    def update_sport(self, sport_id: str, sport_data: dict):
        self._check_profile_data(sport_data, update=True)
        with self._database_engine.new_session() as session:
            sport_dao = SportDAO(session)
            sport = sport_dao.get(sport_id)
            sport = sport_dao.update(sport, sport_data)
            return sport.to_dict()

    def delete_sport(self, sport_id: str):
        with self._database_engine.new_session() as session:
            sport_dao = SportDAO(session)
            sport = sport_dao.get(sport_id)
            sport_dao.delete(sport)

    def search_sport(self, name: str):
        # Query database
        with self._database_engine.new_session() as session:
            sport_dao = SportDAO(session)
            sport = sport_dao.get_by_name(name)
            return sport.to_dict()

    def _check_profile_data(self, data, update=False):
        mandatories = {
            'name': {"type": str},
            'description': {"type": str}
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
