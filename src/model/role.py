from common.database import Database
from model.db_object import DbObject

__author__ = 'smok'

class Role(DbObject):
    def __init__(self, role_name, _id):
        super().__init__(True, False, _id)
        self.role_name = role_name

    @classmethod
    def get_by_role_name(cls, role_name):
        data = Database.find_one("roles", {"role_name": role_name})
        if data is not None:
            return cls(**data)
        return None

    @classmethod
    def get_by_user_type(cls, user_type):
        data = Database.find("roles", {})
        roles = [cls(**elem) for elem in data]
        result = [role for role in roles if role.role_name[5:]==user_type.upper()]
        return None if len(result)==0 else result[0]

    def json(self):
        return {
            "id": self._id,
            "name": self.role_name
        }