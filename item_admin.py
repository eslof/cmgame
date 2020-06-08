from item_db import ItemDB
from item_properties import ITEM_TABLES, ItemAttr


class ItemAdmin(ItemDB):
    @classmethod
    def table_count(cls, table_name: ITEM_TABLES) -> int:
        cls.connect()
        return next(
            iter(
                cls.cur.execute(f"SELECT count(ROWID) FROM {table_name}")
                .fetchone()
                .values()
            )
        )

    @classmethod
    def create_tables(cls):
        with open("item_tables.sql") as if_not_exists:
            cls.cur.executescript(if_not_exists.read())

    @classmethod
    def upsert_bundle(
        cls, table_name: ITEM_TABLES, bundle_name: str, version: int,
    ) -> list:
        cls.connect(False)
        query = (
            f"INSERT INTO {table_name} ({ItemAttr.BUNDLE}, {ItemAttr.VERSION})"
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
