from common.database import Database

class InitDb(object):

    def __init__(self):
        Database.initialize()

    @staticmethod
    def create_admin_user():
        data = Database.find("users", {})
        # add master user if does not exist
        if len(data) == 0:
            Database.insert("users",
                            {"_id": "404a4558725e4e1fb12dca5094c69729", "username": "smok", "user_type": "admin",
                             "role": "ROLE_ADMIN", "first_name": "Jaroslaw", "last_name": "Smorczewski",
                             "email": "jsmorczewski@gmail.com", "active": True, "deleted": False,
                             "password": "$pbkdf2-sha512$25000$QiiF0BojBMDY.3/vvRdibA$0GoqRw3QggvfVwwFLGkfxMOEFQJKxHV.qB95m4PM69AxOpKJdI3yxHg7mokXkOB2qt.nPohPMypVejDs/b7a0A"})

    @staticmethod
    def add_roles():
        data = Database.find("roles", {})
        # add all roles
        if len(data) == 0:
            Database.insert("roles", {'_id': 1, 'role_name': 'ROLE_ADMIN'})
            Database.insert("roles", {'_id': 2, 'role_name': 'ROLE_PLAYER'})


def main():
    print("This script will initialize database with admin user and roles "
          "and create DB file in test folder, move it to src if you want to use it.")
    d = InitDb()
    d.create_admin_user()
    d.add_roles()

    print("Database initialized, verifying...")
    data = Database.find("users", {})
    print(data)

if __name__ == "__main__":
    main()
