import random
import sqlite3

from internal import end
from item_properties import ITEM_DB_PATH


class ItemDB:
    conn: sqlite3.Connection = None
    cur: sqlite3.Cursor = None

    @classmethod
    def close(cls):
        cls.cur.close()
        cls.conn.close()

    @staticmethod
    def dict_factory(cursor: sqlite3.Cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    @staticmethod
    def seeded_random(string1, string2):
        return random.randint(-1, 1)

    @classmethod
    def connect(cls, readonly: bool = True) -> None:
        if not cls.conn:
            try:
                cls.conn = sqlite3.connect(
                    f"file:{ITEM_DB_PATH}?{'mode=ro' if readonly else 'mode=rw'}",
                    uri=True,
                )
            except sqlite3.Error as e:
                end(f"Item DB API (CONNECT): {e}")
            else:
                cls.conn.create_collation("seeded_random", cls.seeded_random)
                cls.conn.row_factory = cls.dict_factory
                cls.cur = cls.conn.cursor()
