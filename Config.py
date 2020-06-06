import json
from typing import NamedTuple


class ConfigAttr(NamedTuple):
    ITEM_COUNT: int
    BIODOME_COUNT: int


Config: ConfigAttr

with open("D:/Projects/cmgame/config.json") as cfg:
    Config = ConfigAttr(**json.load(cfg))
