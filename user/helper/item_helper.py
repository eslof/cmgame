from typing import List, Dict

from item_factory import Items, DBItem

# TODO: look into how to do this better
from properties import starting_inventory


class ItemHelper(Items):
    @staticmethod
    def welcome_info() -> Dict[str, List[DBItem]]:
        # TODO: no hard cody
        return {
            "biodomes": ItemHelper.get_biodomes(),
            "inventory": ItemHelper.get_starter_inventory(),
        }

    @classmethod
    def get_biodomes(cls) -> List[DBItem]:
        cls.connect()
        return cls.cur.execute("SELECT bundle, version FROM biodome").fetchall()

    @classmethod
    def get_starter_inventory(cls) -> List[DBItem]:
        cls.connect()
        sql = f"SELECT bundle, version FROM items WHERE id in ({','.join(['?']*len(starting_inventory))})"
        return cls.cur.execute(sql, starting_inventory).fetchall()

    @classmethod
    def get_inventory(cls, user_inventory: List[int]):
        cls.connect()
        sql = f"SELECT bundle, version FROM items WHERE id in ({','.join(['?']*len(user_inventory))})"
        return cls.cur.execute(sql, user_inventory).fetchall()
