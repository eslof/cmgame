import pathlib
from typing import TypedDict, Literal

ITEM_DB_PATH = "///D:/Projects/cmgame/db.sqlite"  # "db.sqlite"
ITEM_TABLES = Literal["item", "biodome"]


class ItemAttr:
    BUNDLE = "bundle"
    VERSION = "version"


class DBItem(TypedDict):
    bundle: str
    version: int
