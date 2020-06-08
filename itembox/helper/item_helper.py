import random
from typing import List, Dict

from config import Config
from item_db import ItemDB
from item_properties import DBItem
from properties import Constants


class ItemHelper(ItemDB):
    @classmethod
    def get_itembox(cls, seed: str) -> List[DBItem]:
        cls.connect()
        random.seed(seed)
        return cls.conn.execute(
            "SELECT bundle, version FROM item"
            " ORDER BY CAST(id as TEXT) COLLATE seeded_random"
            f" LIMIT {Config.ITEM_BOX_SIZE}"
        ).fetchall()

    @classmethod
    def get_choice_id(cls, choice: int, seed: str) -> int:
        cls.connect()
        random.seed(seed)
        return next(
            iter(
                cls.conn.execute(
                    f"SELECT id FROM item ORDER BY CAST(id as TEXT) COLLATE seeded_random LIMIT 1 OFFSET {choice-1}"
                )
                .fetchone()
                .values()
            )
        )

    @staticmethod
    def itembox_seed(user_id: str, used_key_count: int) -> str:
        return f"{user_id}{used_key_count}"
