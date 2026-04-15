import unittest

from common.database import Database


class InitDbTestCase(unittest.TestCase):

    def setUp(self):
        Database.initialize()

    def test_create_admin_user(self):
        data = Database.find("users", {})
        self.assertIsNotNone(data)
        # add master user if does not exist
        if len(data) == 0:
            Database.insert("users",
                            {"_id": "", "username": "", "user_type": "admin",
                             "role": "ROLE_ADMIN", "first_name": "", "last_name": "",
                             "email": "", "active": True, "deleted": False,
                             "password": ""})

    def test_add_roles(self):
        data = Database.find("roles", {})
        self.assertIsNotNone(data)
        # add all roles
        Database.insert("roles", {'_id': 1, 'role_name': 'ROLE_ADMIN'})
        Database.insert("roles", {'_id': 2, 'role_name': 'ROLE_PLAYER'})
