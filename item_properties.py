import pathlib
from typing import TypedDict, Literal

ITEM_DB_PATH = "///D:/Projects/cmgame/db.sqlite"  # "db.sqlite"


class ItemAttr:
    BUNDLE = "bundle"
    VERSION = "version"


ITEM_TABLES = Literal["item", "biodome"]


class DBItem(TypedDict):
    bundle: str
    version: int
