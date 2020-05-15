import json
import random
import string
from properties import Constants, ResponseField, ItemAttr


# TODO: look into how to do this better


class Item:
    """Class provided to deal with a TODO: proper item database"""

    data = {}

    @classmethod
    def load(cls) -> None:
        """Load/Connect to DB"""
        if not cls.data:
            with open("item_db.json", "r") as file_stream:
                cls.data = json.load(file_stream)

    @classmethod
    def get(cls, item_id: str) -> dict:
        """Get item data"""
        cls.load()
        return cls.data[item_id]

    @classmethod
    def get_template(cls, item_id: str) -> dict:
        item = cls.get(item_id)
        return {
            ResponseField.Item.BUNDLE: item[ItemAttr.BUNDLE],
            ResponseField.Item.VERSION: item[ItemAttr.VERSION],
        }

    @classmethod
    def get_random(cls, count: int, seed: str, exclude_list: list = None):
        """Get random items by given seed and given count, excluding those present in given exclude list."""
        cls.load()
        exclude_list = exclude_list or []
        item_ids = list(cls.data.keys())
        random.Random(seed).shuffle(item_ids)
        filtered_list = list(set(item_ids) - set(exclude_list))
        choices = []
        for i in range(count):
            if len(filtered_list) - len(exclude_list) > 0:
                choices.append(cls.data[filtered_list.pop(0)])

        return choices

    @staticmethod
    def generate_item_id() -> str:
        """TODO: This needs to be looked at"""
        letters = string.ascii_letters + string.digits
        return "".join(
            random.choice(letters) for i in range(Constants.Item.ID_CHAR_LENGTH)
        )
