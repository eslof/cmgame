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

    @staticmethod
    def get_biodomes() -> List[DBItem]:
        return ItemDB.get_many("biodome")

    @staticmethod
    def get_starter_inventory() -> List[DBItem]:
        return ItemDB.get_many("item", Config.STARTING_INVENTORY)

    @staticmethod
    def get_inventory(user_inventory: List[int]) -> List[DBItem]:
        return ItemDB.get_many("item", user_inventory)
