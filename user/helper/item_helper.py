from typing import List, Optional

from config import Config
from item_db import ItemDB
from item_properties import DBItem, ITEM_TABLES, ItemAttr


class ItemHelper:
    @staticmethod
    def get_many(
        item_type: ITEM_TABLES, id_list: Optional[List[int]] = None
    ) -> List[DBItem]:
        ItemDB.connect()
        sql = f"SELECT {ItemAttr.BUNDLE}, {ItemAttr.VERSION} FROM {item_type}"
        if id_list:
            sql = f"{sql} WHERE id IN ({','.join(['?'] * len(id_list))})"
            return ItemDB.cur.execute(sql, id_list).fetchall()
        return ItemDB.cur.execute(sql).fetchall()

    @classmethod
    def get_biodomes(cls) -> List[DBItem]:
        return cls.get_many("biodome")

    @classmethod
    def get_starter_inventory(cls) -> List[DBItem]:
        return cls.get_many("item", Config.STARTING_INVENTORY)

    @classmethod
    def get_inventory(cls, user_inventory: List[int]) -> List[DBItem]:
        return cls.get_many("item", user_inventory)
