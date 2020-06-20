import unittest
import uuid

from exceptions import Error, InvalidData, ResourceNotFound
from controller.person_controller import PersonController
from controller.sport_controller import SportController
from model.database import DatabaseEngine
from model.mapping.person import Person
from model.mapping.user import User
from model.mapping.sport import Sport
from model.mapping.sport_association import SportAssociation


class TestPersonController(unittest.TestCase):
    """
    Unit Tests sport controller
    https://docs.python.org/fr/3/library/unittest.html
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._database_engine = DatabaseEngine()
        cls._database_engine.create_database()
        with cls._database_engine.new_session() as session:
            # Person
            # Password is 'password'
            john = Person(id=str(uuid.uuid4()),
                          firstname="john",
                          lastname="do",
                          email="john.do@mail.com",
                          user=User(username="john",
                                    password_hash='5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
                                    admin=False)
                          )
            session.add(john)

            # Sport to test person-sport association
            swimming = Sport(id=str(uuid.uuid4()), name="Swimming", description="Water", persons=[])
            session.add(swimming)
            session.flush()

            session.flush()
            cls.john_id = john.id

    def setUp(self) -> None:
        """
        Function called before each test
        """
        self.person_controller = PersonController(self._database_engine)

    def test_list_persons(self):
        persons = self.person_controller.list_persons()
        self.assertGreaterEqual(len(persons), 1)

    def test_get_person(self):
        person = self.person_controller.get_person(self.john_id)
        self.assertEqual(person['firstname'], "john")
        self.assertEqual(person['lastname'], "do")
        self.assertEqual(person['id'], self.john_id)

    def test_get_person_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.get_person(str(uuid.uuid4()))

    def test_create_person(self):
        data = {
            "firstname": "Han",
            "lastname": "Solo",
            "email": "han.solo@star.com"
        }
        person_data = self.person_controller.create_person(data)
        self.assertIn('id', person_data)
        self.assertEqual(data['firstname'], person_data['firstname'])
        self.assertEqual(data['lastname'], person_data['lastname'])
        self.assertEqual(data['email'], person_data['email'])

    def test_create_person_missing_data(self):
        data = {}
        with self.assertRaises(InvalidData):
            self.person_controller.create_person(data)

    def test_create_person_error_already_exists(self):
        data = {"firstname": "john", "lastname": "do", "email": "john.do@hostmail.fr"}
        with self.assertRaises(Error):
            self.person_controller.create_person(data)

    def test_update_person(self):
        person_data = self.person_controller.update_person(
            self.john_id, {"email": "john.do@updated.com"})
        self.assertEqual(person_data['email'], "john.do@updated.com")

    def test_update_person_invalid_data(self):
        with self.assertRaises(InvalidData):
            self.person_controller.update_person(self.john_id, {"email": "test"})

    def test_update_person_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.update_person("test", {"description": "test foot"})

    def test_delete_person(self):
        with self._database_engine.new_session() as session:
            rob = Person(id=str(uuid.uuid4()), firstname="rob", lastname="stark",
                         email="rob.stark@winterfell.com")
            session.add(rob)
            session.flush()
            rob_id = rob.id

        self.person_controller.delete_person(rob_id)
        with self.assertRaises(ResourceNotFound):
            self.person_controller.delete_person(rob_id)

    def test_delete_person_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.delete_person(str(uuid.uuid4()))

    def test_search_person(self):
        person = self.person_controller.search_person("john", "do")
        self.assertEqual(person['id'], self.john_id)

    def test_search_person_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.person_controller.search_person("john", "snow")

    def test_search_person_by_username(self):
        person = self.person_controller.get_person_by_username("john")
        self.assertEqual(person['firstname'], "john")
        self.assertEqual(person['lastname'], "do")
        self.assertEqual(person['id'], self.john_id)

    def test_add_delete_sport(self):
        # Test to add a sport to a person
        sport_controller = SportController(self._database_engine)
        sport = sport_controller.search_sport("Swimming")

        # Add
        self.person_controller.add_person_sport(self.john_id, sport.get('id'), "Master")
        person = self.person_controller.get_person_by_username("john")
        sport = sport_controller.search_sport("Swimming")
        self.assertNotEqual(person.get('sports'), [])

        # Delete
        self.person_controller.delete_person_sport(self.john_id, sport.get('id'))
        person = self.person_controller.get_person_by_username("john")
        sport = sport_controller.search_sport("Swimming")
        self.assertEqual(person.get('sports'), [])


if __name__ == '__main__':
    unittest.main()
