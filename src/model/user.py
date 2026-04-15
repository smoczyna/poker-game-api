import uuid

from model.db_object import DbObject
from model.image import Image
from model.role import Role
from src.common.database import Database
from src.common.utils import Utils
from src.common.errors import UserNotExistsError, IncorrectPasswordError, UserAlreadyRegistered, InvalidEmailError

__author__ = 'smok'

class User(DbObject):

    def __init__(self, username, user_type, role, email, first_name, last_name, active, deleted, password=None, _id=None):
        super().__init__(active, deleted, _id)
        self.username = username
        self.password = '' if password is None else password
        self.user_type = user_type
        self.roles = Role.get_by_role_name(role)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_all(cls):
        data = Database.find("users", {})
        if data is not None:
            return [cls(**elem) for elem in data]
        return None

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)
        return None

    @classmethod
    def get_by_id(cls, id):
        data = Database.find_one("users", {"_id": id})
        if data is not None:
            return cls(**data)
        return None

    @classmethod
    def get_by_type(cls, user_type):
        data = Database.find("users", {"user_type": user_type})
        if data is not None:
            return [cls(**elem) for elem in data]
        return None

    @classmethod
    def get_active_by_type(cls, user_type):
        data = Database.find("users", {"active": True, "type": user_type})
        if data is not None:
            return cls(**data)
        return None

    @staticmethod
    def is_login_valid1(username, password):
        user_data = Database.find_one("users", {"username": username})
        if user_data is None:
            raise UserNotExistsError('There is no such user registered yet')

        if not Utils.verify_hashed_password(password, user_data['password']):
            raise IncorrectPasswordError('Given password does no much')

        return user_data['_id']

    @staticmethod
    def is_login_valid2(email, password):
        user_data = Database.find_one("users", {"email": email})
        if user_data is None:
            raise UserNotExistsError('There is no such user registered yet')

        if not Utils.verify_hashed_password(password, user_data['password']):
            raise IncorrectPasswordError('Given password does no much')

        return user_data['_id']

    @staticmethod
    def register(username, email, user_type, password, first_name, last_name, birth_date, gender, phone, address):
        """
        registers the user in the system
        password doesn't come hashed with sha512, it is hashed at the end
        """
        user_data = Database.find_one("users", {"email": email})
        if user_data is not None:
            raise UserAlreadyRegistered('Given email is already registered in the system')

        if not Utils.is_email_valid(email):
            raise InvalidEmailError('Given email has incorrect format')

        role = Role.get_by_user_type(user_type)
        user = User(username, user_type, role.role_name, email, Utils.hash_password(password), first_name, last_name, True, False)
        Database.insert("users", user.json())
        #TODO: return something more meaningful than True
        return True

    def resolve_roles(self):
        if self.roles is not None and type(self.roles) == str:
            return self.roles
        else:
            return None

    # def json(self):
    #     return {
    #         "_id": self._id,
    #         "username": self.username,
    #         "user_type": self.user_type,
    #         "role": self.resolve_roles(),
    #         "email": self.email,
    #         "password": self.password,
    #         "first_name": self.first_name,
    #         "last_name": self.last_name,
    #         "active": self.active,
    #         "deleted": self.deleted
    #     }
    #
    # def json_rest(self):
    #     return {
    #         "id": self._id,
    #         "username": self.username,
    #         "userName": self.username,
    #         "userType": self.user_type,
    #         "type": self.user_type,
    #         "role": self.resolve_roles(),
    #         "email": self.email,
    #         "firstName": self.first_name,
    #         "lastName": self.last_name,
    #         "active": self.active,
    #         "deleted": self.deleted
    #     }

    def insert_user(self):
        Database.insert("users", self.json())

    # @staticmethod
    # def create_user_from_json(data):
    #     user = User(data['username'],
    #                 data['user_type'],
    #                 data['roles'],
    #                 data['email'],
    #                 data['password'],
    #                 data['_id'])
    #     return user


class LoggedUser(User):

    def __init__(self, user, is_authenticated, token):
        self.username = user.username
        self.user_type = user.user_type
        self.email = user.email
        self.roles = [user.roles]
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.password = user.password
        self.is_authenticated = is_authenticated
        self.token = token

    def json(self):
        return {
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "type": self.user_type,
            "roles": [role.json() for role in self.roles] if not None else [],
            "isAuthenticated": self.is_authenticated,
            "token": self.token
        }

    @staticmethod
    def upload_user_image(user_id, image_file):
        image = Image(user_id, image_file)
        image.save_to_mongo()

    @staticmethod
    def replace_user_image(user_id, image):
        Image.replace_member_image(user_id, image)