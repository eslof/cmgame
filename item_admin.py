from typing import Optional

from item_db import ItemDB
from item_properties import ITEM_TABLES, ItemAttr


class ItemAdmin:
    @staticmethod
    def table_count(table_name: ITEM_TABLES) -> int:
        ItemDB.connect()
        return next(
            iter(
                ItemDB.cur.execute(f"SELECT count(ROWID) FROM {table_name}")
                .fetchone()
                .values()
            )
        )

    @staticmethod
    def create_tables() -> None:
        with open("item_tables.sql") as if_not_exists:
            ItemDB.cur.executescript(if_not_exists.read())

    @staticmethod
    def upsert_bundle(table_name: ITEM_TABLES, bundle_name: str, version: int) -> None:
        ItemDB.connect(False)
        ItemDB.cur.execute(
            f"INSERT INTO {table_name} ({ItemAttr.BUNDLE}, {ItemAttr.VERSION})"
            f" VALUES('{bundle_name}', {version})"
            f" ON CONFLICT({ItemAttr.BUNDLE})"
            f" DO UPDATE SET {ItemAttr.VERSION} = {version}"
        )

    @staticmethod
    def change_bundle_name(
        table: str, old_name: str, new_name: str, version: Optional[int] = None
    ) -> None:
        ItemDB.connect(False)
        ItemDB.cur.execute(
            f"UPDATE {table}"
            f" SET {ItemAttr.BUNDLE}='{new_name}', {ItemAttr.VERSION}={version or ItemAttr.VERSION}"
            f" WHERE {ItemAttr.BUNDLE}='{old_name}'"
        )


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
