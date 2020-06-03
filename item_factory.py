import sqlite3
import random
import sqlite3
from typing import Dict, Final, Literal
from typing import TypedDict

# TODO: look into this
from internal import end

AUTO: Final = "auto"
ITEMS: Final = "items"
BUNDLE = Literal["bundle"]
VERSION = Literal["version"]
BIODOMES: Final = "biodomes"


def seeded_random(string1, string2):
    return random.randint(-1, 1)


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
    # data: ItemDB = None
    conn: sqlite3.Connection = None
    cur: sqlite3.Cursor = None

    # SQL_CREATE_ITEM_TABLE = """ CREATE TABLE IF NOT EXISTS items (
    #                         id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                         bundle TEXT NOT NULL,
    #                         version INTEGER NOT NULL,
    #                         UNIQUE (bundle)
    #                     );"""
    # create_table = """CREATE TABLE IF NOT EXISTS biodome (
    #                     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #                     bundle TEXT NOT NULL,
    #                     version INTEGER NOT NULL,
    #                     UNIQUE (bundle)
    #                 );"""

    @classmethod
    def connect(cls, readonly: bool = True) -> None:
        if not cls.conn:
            try:
                cls.conn = sqlite3.connect(
                    f"file:db.sqlite{'?mode=ro' if readonly else ''}", uri=True
                )
            except sqlite3.Error as e:
                end(f"Item DB API ({type(e).__name__})")
            else:
                cls.conn.create_collation("seeded_random", seeded_random)
                cls.conn.row_factory = sqlite3.Row
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


# random.seed("hwefawefalo")
# Items.connect()
# mysql = "SELECT id FROM items ORDER BY CAST(id as TEXT) COLLATE seeded_random LIMIT 3 OFFSET 2"
# results = Items.cur.execute(mysql).fetchone()
# print(results)
# print(results.keys())
# print(tuple(results)[0])
#
# items = [{row.keys()[i]: tuple(row)[i] for i in range(len(row))} for row in results]
# print(items)
