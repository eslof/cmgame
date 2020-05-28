from typing import List
from item_factory import Items, DBItem, BUNDLE, VERSION


# TODO: look into how to do this better
from properties import starting_inventory


class ItemHelper(Items):
    @classmethod
    def template_inv(cls, item_id: int) -> DBItem:
        cls.load_data()
        item = cls.data["items"][item_id]
        return {
            BUNDLE: item["bundle"],
            VERSION: item["version"],
        }

    @classmethod
    def get_biodomes(cls) -> List[DBItem]:
        cls.load_data()
        biodomes = list(cls.data["biodomes"].values())
        return biodomes

    @classmethod
    def get_starter_inventory(cls) -> List[DBItem]:
        cls.load_data()
        return [cls.data["items"][i] for i in starting_inventory]
