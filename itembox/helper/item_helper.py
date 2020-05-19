import json
import random
import string
from decimal import Decimal

from properties import Constants, ResponseField, ItemAttr, Seed


# TODO: look into how to do this better


class ItemHelper:
    """Class provided to deal with a TODO: proper item database"""

    data = {}

    @classmethod
    def itembox(cls, count: int, seed: str, exclude_list: list = None):
        """Get random items by given seed and given count, excluding those present in given exclude list."""
        cls.load_data()
        exclude_list = exclude_list or []
        item_ids = list(cls.data.keys())
        random.Random(seed).shuffle(item_ids)
        filtered_list = list(set(item_ids) - set(exclude_list))
        choices = []
        for i in range(count):
            if len(filtered_list) - len(exclude_list) > 0:
                choices.append(cls.data[filtered_list.pop(0)])

        return choices

    @classmethod
    def load_data(cls) -> None:
        """Load/Connect to DB"""
        if not cls.data:
            with open("../../item_db.json", "r") as file_stream:
                cls.data = json.load(file_stream)

    @staticmethod
    def itembox_seed(user_id: str, key_count: int, used_key_count: int):
        id_hash = 0
        id_len = len(user_id)
        for i in range(id_len):
            id_hash += ord(user_id[i]) * (i + 1)

        return id_hash + Seed.ITEMBOX + key_count + used_key_count
