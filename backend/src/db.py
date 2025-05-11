import shelve
from typing import Any
import os


class ShelveDB:
    def __init__(self, db_name: str):
        self.db_path = os.path.join(os.path.dirname(__file__), "db")
        os.makedirs(self.db_path, exist_ok=True)
        self.db_name = db_name

    def write(self, key: str, value: Any):
        with shelve.open(os.path.join(self.db_path, self.db_name)) as db:
            db[key] = value

    def read(self, key: str) -> Any:
        with shelve.open(os.path.join(self.db_path, self.db_name)) as db:
            return db.get(key)

    def delete(self, key: str):
        with shelve.open(os.path.join(self.db_path, self.db_name)) as db:
            if key in db:
                del db[key]

    def list_keys(self):
        with shelve.open(os.path.join(self.db_path, self.db_name)) as db:
            return list(db.keys())
        
    def read_all(self):
        with shelve.open(os.path.join(self.db_path, self.db_name)) as db:
            return dict(db)