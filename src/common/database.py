import json
import os
import sqlite3
from typing import Any, Dict, Iterable, List, Optional

__author__ = "smok"


class Database(object):
    DB_NAME = "pokergame.db"
    DB_DIR = os.path.join(os.getcwd())
    DB_PATH = os.path.join(DB_DIR, DB_NAME)
    CONNECTION = None

    DEFAULT_TABLES = ("users", "roles", "games")

    @staticmethod
    def initialize():
        if Database.CONNECTION is None:
            os.makedirs(Database.DB_DIR, exist_ok=True)
            # Database.CONNECTION = sqlite3.connect(Database.DB_PATH)
            Database.CONNECTION = sqlite3.connect(Database.DB_PATH, check_same_thread=False)
            Database.CONNECTION.row_factory = sqlite3.Row
            Database._create_default_tables()
            print(f"Connected to SQLite DB: {Database.DB_PATH}")

    @staticmethod
    def _conn():
        if Database.CONNECTION is None:
            Database.initialize()
        return Database.CONNECTION

    @staticmethod
    def _create_default_tables():
        conn = Database._conn()
        for table in Database.DEFAULT_TABLES:
            conn.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document TEXT NOT NULL
                )
                """
            )
        conn.commit()

    @staticmethod
    def _normalize_table_name(collection: str) -> str:
        if not collection or not isinstance(collection, str):
            raise ValueError("Table name must be a non-empty string")
        return collection

    @staticmethod
    def _doc_matches(document: Dict[str, Any], query: Dict[str, Any]) -> bool:
        for key, value in query.items():
            if document.get(key) != value:
                return False
        return True

    @staticmethod
    def _fetch_documents(collection: str) -> List[Dict[str, Any]]:
        conn = Database._conn()
        table = Database._normalize_table_name(collection)
        cursor = conn.execute(f"SELECT document FROM {table}")
        return [json.loads(row["document"]) for row in cursor.fetchall()]

    @staticmethod
    def get_db(collection):
        return Database._fetch_documents(collection)

    @staticmethod
    def get_db_fs():
        raise NotImplementedError("SQLite does not support GridFS-style file storage.")

    @staticmethod
    def insert(collection, data):
        conn = Database._conn()
        table = Database._normalize_table_name(collection)
        conn.execute(
            f"INSERT INTO {table} (document) VALUES (?)",
            (json.dumps(data),)
        )
        conn.commit()

    @staticmethod
    def insert_many(collection, data):
        conn = Database._conn()
        table = Database._normalize_table_name(collection)
        conn.executemany(
            f"INSERT INTO {table} (document) VALUES (?)",
            [(json.dumps(item),) for item in data]
        )
        conn.commit()

    @staticmethod
    def find(collection, query):
        documents = Database._fetch_documents(collection)
        return [doc for doc in documents if Database._doc_matches(doc, query)]

    @staticmethod
    def find_one(collection, query):
        results = Database.find(collection, query)
        return results[0] if results else None

    @staticmethod
    def find_aggr(collection, query, predict):
        # Mongo-style projection/aggregation is not implemented here.
        # This returns filtered documents to preserve basic compatibility.
        return Database.find(collection, query)

    @staticmethod
    def count(collection, query):
        return len(Database.find(collection, query))

    @staticmethod
    def update(collection, query, payload):
        conn = Database._conn()
        table = Database._normalize_table_name(collection)
        cursor = conn.execute(f"SELECT id, document FROM {table}")
        rows = cursor.fetchall()

        updated = 0
        for row in rows:
            doc = json.loads(row["document"])
            if Database._doc_matches(doc, query):
                doc.update(payload)
                conn.execute(
                    f"UPDATE {table} SET document = ? WHERE id = ?",
                    (json.dumps(doc), row["id"])
                )
                updated += 1
                break

        conn.commit()
        return updated

    @staticmethod
    def delete(collection, query):
        conn = Database._conn()
        table = Database._normalize_table_name(collection)
        cursor = conn.execute(f"SELECT id, document FROM {table}")
        rows = cursor.fetchall()

        deleted = 0
        for row in rows:
            doc = json.loads(row["document"])
            if Database._doc_matches(doc, query):
                conn.execute(f"DELETE FROM {table} WHERE id = ?", (row["id"],))
                deleted += 1
                break

        conn.commit()
        return deleted
