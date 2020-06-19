import unittest
import uuid

from exceptions import Error, InvalidData, ResourceNotFound
from controller.user_controller import UserController
from model.database import DatabaseEngine
from model.mapping.person import Person
from model.mapping.user import User


class TestUserController(unittest.TestCase):
    """
    Unit Tests sport controller
    https://docs.python.org/fr/3/library/unittest.html
    """

    @classmethod
    def setUpClass(cls) -> None:
        cls._database_engine = DatabaseEngine()
        cls._database_engine.create_database()
        with cls._database_engine.new_session() as session:
            # User
            # Password is 'password'
            bobby = User(id=str(uuid.uuid4()), username='bobby',
                         password_hash='5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', admin=False)
            session.add(bobby)
            session.flush()
            cls.bobby_id = bobby.id

    def setUp(self) -> None:
        """
        Function called before each test
        """
        self.user_controller = UserController(self._database_engine)

    def test_list_users(self):
        users = self.user_controller.list_users()
        self.assertGreaterEqual(len(users), 1)

    def test_get_user(self):
        user = self.user_controller.get_user(self.bobby_id)
        self.assertEqual(user['username'], "bobby")
        self.assertEqual(user['password_hash'], "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8")
        self.assertEqual(user['id'], self.bobby_id)

    def test_get_person_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.user_controller.get_user(str(uuid.uuid4()))

    def test_create_user(self):
        data = {
            "username": "toto",
            "password": "titi"
        }
        user_data = self.user_controller.create_user(data)
        self.assertIn('id', user_data)
        self.assertEqual(data['username'], user_data['username'])
        self.assertEqual(user_data['password_hash'], 'cce66316b4c1c59df94a35afb80cecd82d1a8d91b554022557e115f5c275f515')
        self.assertFalse(user_data['admin'])

    def test_create_user_missing_data(self):
        data = {}
        with self.assertRaises(InvalidData):
            self.user_controller.create_user(data)

    def test_create_user_error_already_exists(self):
        data = {"username": "bobby", "password": "password"}
        with self.assertRaises(Error):
            self.user_controller.create_user(data)

    def test_update_user(self):
        user_data = self.user_controller.update_user(
            self.bobby_id, {"username": "bybbo"})
        self.assertEqual(user_data['username'], "bybbo")

    def test_update_user_invalid_data(self):
        with self.assertRaises(InvalidData):
            self.user_controller.update_user(self.bobby_id, {"password": 12})

    def test_update_user_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.user_controller.update_user("test", {"username": "bilboquet"})

    def test_delete_user(self):
        with self._database_engine.new_session() as session:
            billy = User(id=str(uuid.uuid4()), username='billy')
            billy.hash_password('password')
            session.add(billy)
            session.flush()
            billy_id = billy.id

        self.user_controller.delete_user(billy_id)
        with self.assertRaises(ResourceNotFound):
            self.user_controller.delete_user(billy_id)

    def test_delete_user_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.user_controller.delete_user(str(uuid.uuid4()))

    def test_search_user(self):
        user = self.user_controller.search_user("bobby")
        self.assertEqual(user['id'], self.bobby_id)

    def test_search_user_not_exists(self):
        with self.assertRaises(ResourceNotFound):
            self.user_controller.search_user("carbonara")

    def test_hash_password(self):
        usr = User(username="usr")
        usr.hash_password('password')
        self.assertEqual(usr.password_hash, '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')

    def test_check_password(self):
        user = User(username='belette')
        user.hash_password('super_belette')
        self.assertTrue(user.check_password('super_belette'))


if __name__ == '__main__':
    unittest.main()
