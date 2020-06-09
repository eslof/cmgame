import random
import sqlite3

from internal import end
from item_properties import ITEM_DB_PATH


class _ItemDB:
    conn: sqlite3.Connection = None
    cur: sqlite3.Cursor = None

    def __del__(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    @staticmethod
    def dict_factory(cursor: sqlite3.Cursor, row):
        return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

    @staticmethod
    def seeded_random(string1, string2):
        """random.seed() then ORDER BY CAST(id as TEXT) COLLATE seeded_random"""
        return random.randint(-1, 1)

    def connect(self, readonly: bool = True) -> None:
        if not self.conn:
            try:
                self.conn = sqlite3.connect(
                    f"file:{ITEM_DB_PATH}?{'mode=ro' if readonly else 'mode=rw'}",
                    uri=True,
                )
            except sqlite3.Error as e:
                end(f"Item DB API (CONNECT): {e}")
            else:
                self.conn.create_collation("seeded_random", self.seeded_random)
                self.conn.row_factory = self.dict_factory
                self.cur = self.conn.cursor()


ItemDB = _ItemDB()
