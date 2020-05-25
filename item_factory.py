import json
from typing import Optional, Dict, Union, cast

from database import ItemAttr


class ItemFactory:
    data: Dict[str, Dict[str, Union[str, int]]]
    next_auto: int

    @classmethod
    def save_data(cls) -> None:
        save_data = cast(Dict[str, Union[int, Dict[str, Union[str, int]]]], cls.data)
        save_data["next_auto"] = cls.next_auto
        with open("../../item_db.json", "w") as file_stream:
            file_stream.write(json.dumps(cls.data))

    @classmethod
    def load_data(cls) -> None:
        """Load/Connect to DB"""
        if not cls.data:
            with open("../../item_db.json", "r") as file_stream:
                data = json.load(file_stream)
                cls.next_auto = data["next_auto"]
                del data["next_auto"]
                cls.data = data

    @classmethod
    def update(cls, bundle_name: str, version: int) -> None:
        cls.load_data()

        def scan() -> Optional[str]:
            for key in cls.data:
                if cls.data[key][ItemAttr.BUNDLE] == bundle_name:
                    return key
            return None

        existing_id = scan()
        item_id: str = existing_id or str(cls.next_auto)
        if item_id == str(cls.next_auto):
            cls.next_auto += 1

        cls.data[item_id] = {
            ItemAttr.BUNDLE: bundle_name,
            ItemAttr.VERSION: version,
        }
