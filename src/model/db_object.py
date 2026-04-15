import uuid
from common.database import Database

__author__ = 'smok'

class DbObject(object):
    def __init__(self, active, deleted, _id=None):
        self.active = active
        self.deleted = deleted
        self._id = uuid.uuid4().hex if _id is None else _id

    def json_id(self):
        return {
            "_id": self._id
        }

    def insert_object(self, table):
        Database.insert(table, self.json())

    def update_object(self, table):
        Database.update(table, self.json_id(), self.json())
