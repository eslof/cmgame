import pathlib
import random
import sqlite3
from typing import Dict, Literal
from typing import TypedDict

from internal import end


class ItemAttr:
    BUNDLE = "bundle"
    VERSION = "version"


class DBItem(TypedDict):
    bundle: str
    version: int


class ItemDB(TypedDict):
    items: Dict[int, DBItem]
    biodomes: Dict[int, DBItem]


class Items:
    conn: sqlite3.Connection = None
    cur: sqlite3.Cursor = None

    @classmethod
    def create_tables(cls):
        with open("item_tables.sql") as if_not_exists:
            cls.cur.executescript(if_not_exists.read())

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
                print(pathlib.Path().absolute())
                print(
                    f"file:///D:/Projects/cmgame/db.sqlite?{'mode=ro' if readonly else 'mode=rw'}"
                )
                cls.conn = sqlite3.connect(
                    f"file:///D:/Projects/cmgame/db.sqlite?{'mode=ro' if readonly else 'mode=rw'}",
                    uri=True,
                )
            except sqlite3.Error as e:
                end(f"Item DB API ({type(e).__name__})")
            else:
                cls.conn.create_collation("seeded_random", cls.seeded_random)
                cls.conn.row_factory = cls.dict_factory
                cls.cur = cls.conn.cursor()

    @classmethod
    def upsert_bundle(
        cls, item_type: Literal["items", "biodomes"], bundle_name: str, version: int,
    ) -> list:
        cls.connect(False)
        query = (
            f"INSERT INTO {item_type} ({ItemAttr.BUNDLE}, {ItemAttr.VERSION})"
            f" VALUES('{bundle_name}', {version})"
            f" ON CONFLICT({ItemAttr.BUNDLE})"
            f" DO UPDATE SET {ItemAttr.VERSION} = {version}"
        )
        return cls.cur.execute(query).fetchall()

    @classmethod
    def change_bundle_name(cls, table, old_name, new_name, version=None) -> list:
        cls.connect(False)
        query = (
            f"UPDATE {table}"
            f" SET {ItemAttr.BUNDLE}='{new_name}', {ItemAttr.VERSION}={version or ItemAttr.VERSION}"
            f" WHERE {ItemAttr.BUNDLE}='{old_name}'"
        )
        return cls.cur.execute(query).fetchall()


# Items.connect()
# sql = f"SELECT bundle, version FROM items WHERE id in ({','.join(['?'] * len(starting_inventory))})"
# print(Items.cur.execute(sql, starting_inventory).fetchall())
# Items.connect(False)
# Items.create_tables()
# random.seed("hwefawefalo")
# Items.connect()
# random.seed("6")
# sql_many = "SELECT bundle, version FROM items ORDER BY CAST(id as TEXT) COLLATE seeded_random LIMIT 3 OFFSET 3"
# sql_one = "SELECT * FROM items ORDER BY CAST(id as TEXT) COLLATE seeded_random LIMIT 1 OFFSET 3"
# result = Items.cur.execute(sql_one).fetchone()
# print(result)
# print(result.keys())
# results = Items.cur.execute(sql_many).fetchall()
# print(results)
# items = [{row.keys()[i]: tuple(row)[i] for i in range(len(row))} for row in results]
# print(items)
