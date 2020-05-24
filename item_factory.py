import json
from typing import Optional, Any, Dict, Union

from database import ItemAttr


class ItemFactory:
    data: Dict[str, Union[int, Dict[str, str]]] = {}

    @classmethod
    def save_data(cls) -> None:
        with open("../../item_db.json", "w") as file_stream:
            file_stream.write(json.dumps(cls.data))

    @classmethod
    def load_data(cls) -> None:
        """Load/Connect to DB"""
        if not cls.data:
            with open("../../item_db.json", "r") as file_stream:
                cls.data = json.load(file_stream)

    @classmethod
    def update(cls, bundle_name: str, version: int) -> None:
        cls.load_data()
        if cls.data:

            def scan() -> Optional[str]:
                for key in cls.data:
                    if key == "next_auto":
                        pass
                    elif (
                        cls.data[key][ItemAttr.BUNDLE] == bundle_name
                    ):  # type: Dict[str, str]
                        return key
                return None

            _scan: Optional[str] = scan()
            item_id: str = _scan or cls.data["next_auto"]
            if not _scan:
                cls.data["next_auto"] += 1

            cls.data[item_id] = {
                ItemAttr.BUNDLE: bundle_name,
                ItemAttr.VERSION: version,
            }
