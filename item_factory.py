import pickle
from typing import Optional, Dict, Final, Literal

from typing import TypedDict

# TODO: look into this
AUTO: Final = "auto"
ITEMS: Final = "items"
BUNDLE: Final = "bundle"
VERSION: Final = "version"
BIODOMES: Final = "biodomes"


class DBItem(TypedDict):
    bundle: str
    version: int


class ItemDB(TypedDict):
    auto: Dict[str, int]
    items: Dict[int, DBItem]
    biodomes: Dict[int, DBItem]


class Items:
    data: ItemDB

    @classmethod
    def save_data(cls) -> None:
        with open("item_db.p", "wb") as file:
            pickle.dump(cls.data, file, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    def load_data(cls) -> None:
        if not cls.data:
            with open("item_db.p", "rb") as file:
                cls.data = pickle.load(file)

    @classmethod
    def update(
        cls, item_type: Literal["items", "biodomes"], bundle_name: str, version: int,
    ) -> None:
        cls.load_data()
        auto = cls.data[AUTO]
        if item_type == "items":
            target = cls.data[ITEMS]
        elif item_type == "biodomes":
            target = cls.data[BIODOMES]
        else:
            raise ValueError

        def scan() -> Optional[int]:
            return next(
                (i for i in target.keys() if target[i][BUNDLE] == bundle_name), None,
            )

        item_id: int = scan() or auto[item_type]
        if item_id == auto[item_type]:
            auto[item_type] += 1

        target[item_id] = {
            BUNDLE: bundle_name,
            VERSION: version,
        }
