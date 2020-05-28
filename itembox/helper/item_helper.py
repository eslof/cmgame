import json
import random
from typing import List, Dict, Union, KeysView

from database import ItemAttr
from item_factory import ItemDB, Items, DBItem


class ItemHelper(Items):
    @classmethod
    def itembox(cls, seed: str, count: int) -> List[DBItem]:
        cls.load_data()
        i_box: List[int] = random.Random(seed).sample(cls.data["items"].keys(), count)
        return [cls.data["items"][i] for i in i_box]

    @classmethod
    def get_choice(cls, choice: int, seed: str, count: int) -> DBItem:
        cls.load_data()
        i_box: List[int] = random.Random(seed).sample(cls.data["items"].keys(), count)
        return cls.data["items"][i_box[choice]]

    @staticmethod
    def itembox_seed(user_id: str, used_key_count: int) -> str:
        return f"{user_id}{used_key_count}"
