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
    def template_inv(cls, item_id: str) -> dict:
        cls.load_data()
        item = cls.get(item_id)
        return {
            ResponseField.Item.BUNDLE: item[ItemAttr.BUNDLE],
            ResponseField.Item.VERSION: item[ItemAttr.VERSION],
        }

    @classmethod
    def get(cls, item_id: str) -> dict:
        cls.load_data()
        return cls.data[item_id]

    @classmethod
    def load_data(cls) -> None:
        """Load/Connect to DB"""
        if not cls.data:
            with open("../../item_db.json", "r") as file_stream:
                cls.data = json.load(file_stream)
