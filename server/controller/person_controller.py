import re

from model.dao.person_dao import PersonDAO
from exceptions import Error, InvalidData


class PersonController:
    """
    Person actions
    """

    def __init__(self, database_engine):
        self._database_engine = database_engine
        self._frames = []

    def list_persons(self):
        with self._database_engine.new_session() as session:
            persons = PersonDAO(session).get_all()
            persons_data = [person.to_dict() for person in persons]
        return persons_data

    def get_person(self, person_id):
        with self._database_engine.new_session() as session:
            person = PersonDAO(session).get(person_id)
            person_data = person.to_dict()
        return person_data

    def get_person_by_name(self, firstname, lastname):
        with self._database_engine.new_session() as session:
            person = PersonDAO(session).get_by_name(firstname, lastname)
            person_data = person.to_dict()
        return person_data

    def create_person(self, data):

        self._check_profile_data(data)
        try:
            with self._database_engine.new_session() as session:
                # Save person in database
                person = PersonDAO(session).create(data)
                person_data = person.to_dict()
                return person_data
        except Error as e:
            # log error
            raise e

    def update_person(self, person_id, person_data):

        self._check_profile_data(person_data, update=True)
        with self._database_engine.new_session() as session:
            person_dao = PersonDAO(session)
            person = person_dao.get(person_id)
            person = person_dao.update(person, person_data)
            return person.to_dict()

    def delete_person(self, person_id):

        with self._database_engine.new_session() as session:
            person_dao = PersonDAO(session)
            person = person_dao.get(person_id)
            person_dao.delete(person)

    def search_person(self, firstname, lastname):

        # Query database
        with self._database_engine.new_session() as session:
            person_dao = PersonDAO(session)
            person = person_dao.get_by_name(firstname, lastname)
            return person.to_dict()

    def _check_profile_data(self, data, update=False):
        name_pattern = re.compile("^[\S-]{2,50}$")
        email_pattern = re.compile("^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$")
        mandatories = {
            'firstname': {"type": str, "regex": name_pattern},
            'lastname': {"type": str, "regex": name_pattern},
            'email': {"type": str, "regex": email_pattern}
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
