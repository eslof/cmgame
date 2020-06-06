import random
from typing import List

from item_factory import Items, DBItem
from properties import Constants


class ItemHelper(Items):
    @classmethod
    def get_itembox(cls, seed: str) -> List[DBItem]:
        cls.connect()
        random.seed(seed)
        results = cls.conn.execute(
            "SELECT bundle, version FROM items"
            " ORDER BY CAST(id as TEXT) COLLATE seeded_random"
            f" LIMIT {Constants.ItemBox.ITEM_COUNT}"
        ).fetchall()
        random.seed()
        return [
            {row.keys()[i]: tuple(row)[i] for i in range(len(row))} for row in results
        ]

    @classmethod
    def get_choice(cls, choice: int, seed: str) -> int:
        cls.connect()
        random.seed(seed)
        row = cls.conn.execute(
            f"SELECT id FROM items ORDER BY CAST(id as TEXT) COLLATE seeded_random LIMIT 1 OFFSET {choice-1}"
        ).fetchone()
        random.seed()
        return tuple(row)[0]

    @staticmethod
    def itembox_seed(user_id: str, used_key_count: int) -> str:
        return f"{user_id}{used_key_count}"
