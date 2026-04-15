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
                            {"_id": "404a4558725e4e1fb12dca5094c69729", "username": "smok", "user_type": "admin",
                             "role": "ROLE_ADMIN", "first_name": "Jaroslaw", "last_name": "Smorczewski",
                             "email": "jsmorczewski@gmail.com", "active": True, "deleted": False,
                             "password": "$pbkdf2-sha512$25000$QiiF0BojBMDY.3/vvRdibA$0GoqRw3QggvfVwwFLGkfxMOEFQJKxHV.qB95m4PM69AxOpKJdI3yxHg7mokXkOB2qt.nPohPMypVejDs/b7a0A"})

    def test_add_roles(self):
        data = Database.find("roles", {})
        self.assertIsNotNone(data)
        # add all roles
        Database.insert("roles", {'_id': 1, 'role_name': 'ROLE_ADMIN'})
        Database.insert("roles", {'_id': 2, 'role_name': 'ROLE_PLAYER'})
