import pickle
from typing import Optional, Dict

from database import ItemAttr

from typing import TypedDict


class DBItem(TypedDict):
    bundle: str
    version: int


class ItemDB(TypedDict):
    auto: int
    items: Dict[int, DBItem]


class Items:
    data: ItemDB

    @classmethod
    def save_data(cls) -> None:
        with open("item_db.p", "wb") as file:
            pickle.dump(cls.data, file, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load_data(cls) -> None:
        if not cls.data:
            with open("../../item_db.p", "rb") as file:
                cls.data = pickle.load(file)

    @classmethod
    def update(cls, bundle_name: str, version: int) -> None:
        cls.load_data()

        def scan() -> Optional[int]:
            return next(
                (
                    i
                    for i in cls.data["items"].keys()
                    if cls.data["items"][i]["bundle"] == bundle_name
                ),
                None,
            )

        item_id: int = scan() or cls.data["auto"]
        if item_id == cls.data["auto"]:
            cls.data["auto"] += 1

        cls.data["items"][item_id] = {
            ItemAttr.BUNDLE: bundle_name,
            ItemAttr.VERSION: version,
        }
