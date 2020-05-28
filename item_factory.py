import pickle
from typing import Optional, Dict, Final, Literal

from typing import TypedDict

# TODO: look into this
AUTO: Final = "auto"
ITEMS: Final = "items"
BUNDLE: Final = "bundle"
VERSION: Final = "version"


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
                    for i in cls.data[ITEMS].keys()
                    if cls.data[ITEMS][i][BUNDLE] == bundle_name
                ),
                None,
            )

        item_id: int = scan() or cls.data[AUTO]
        if item_id == cls.data[AUTO]:
            cls.data[AUTO] += 1

        cls.data[ITEMS][item_id] = {
            BUNDLE: bundle_name,
            VERSION: version,
        }
