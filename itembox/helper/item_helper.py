import json
import random
from typing import List, Any, Dict, Union

from properties import Seed


# TODO: look into how to do this better


class ItemHelper:
    data: Dict[str, Dict[str, str]]
    next_auto: int

    @classmethod
    def itembox(
        cls, count: int, seed: str, exclude_list: List[str]
    ) -> List[Dict[str, str]]:
        cls.load_data()
        item_ids = list(cls.data.keys())
        random.Random(seed).shuffle(item_ids)
        filtered_list = list(set(item_ids) - set(exclude_list))
        choices: List[Dict[str, str]] = []
        for i in range(count):
            if len(filtered_list) - len(exclude_list) > 0:
                choices.append(cls.data[filtered_list.pop(0)])

        return choices

    @classmethod
    def load_data(cls) -> None:
        if not cls.data:
            with open("../../item_db.json", "r") as file_stream:
                data = json.load(file_stream)
                cls.next_auto = data["next_auto"]
                del data["next_auto"]
                cls.data = data

    @staticmethod
    def itembox_seed(user_id: str, key_count: int, used_key_count: int) -> str:
        return f"{key_count}{user_id}{used_key_count}"
