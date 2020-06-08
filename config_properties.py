from typing import NamedTuple, List

CONFIG_JSON_PATH = "D:/Projects/cmgame/config.json"  # "config.json"


class ConfigAttr(NamedTuple):
    BIODOME_COUNT: int = 0
    ITEM_COUNT: int = 0
    GRID_META_LIMIT: int = 2048
    HOME_COUNT_MAX: int = 6
    HOME_META_LIMIT: int = 2048
    ITEM_BOX_SIZE: int = 3
    STARTING_INVENTORY: List[int] = [1, 2, 3, 4]
    STARTING_KEY_COUNT: int = 3
    USER_META_LIMIT: int = 2048
