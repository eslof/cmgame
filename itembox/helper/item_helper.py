import random
from typing import List, Dict

from config import Config
from item_db import ItemDB
from item_properties import DBItem


class ItemHelper:
    @staticmethod
    def get_itembox(seed: str) -> List[DBItem]:
        ItemDB.connect()
        random.seed(seed)
        return ItemDB.cur.execute(
            "SELECT bundle, version FROM item"
            " ORDER BY CAST(id as TEXT) COLLATE seeded_random"
            f" LIMIT {Config.ITEM_BOX_SIZE}"
        ).fetchall()

    @staticmethod
    def get_choice_id(choice: int, seed: str) -> int:
        ItemDB.connect()
        random.seed(seed)
        return next(
            iter(
                ItemDB.cur.execute(
                    f"SELECT id FROM item ORDER BY CAST(id as TEXT) COLLATE seeded_random LIMIT 1 OFFSET {choice-1}"
                )
                .fetchone()
                .values()
            )
        )

    @staticmethod
    def itembox_seed(user_id: str, used_key_count: int) -> str:
        return f"{user_id}{used_key_count}"
