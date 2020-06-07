import json
from typing import NamedTuple, List

from item_factory import Items
from properties import starting_inventory


class ConfigAttr(NamedTuple):
    ITEM_COUNT: int
    BIODOME_COUNT: int
    ITEM_BOX_SIZE: int = 3
    STARTING_INVENTORY: List[int] = starting_inventory


Config: ConfigAttr

with open("D:/Projects/cmgame/config.json") as cfg_r:
    Config = ConfigAttr(**json.load(cfg_r))


def update_config():
    _asdict = Config._asdict()
    Items.connect()
    _asdict["ITEM_COUNT"] = next(
        iter(Items.cur.execute("SELECT count(ROWID) FROM item").fetchone().values())
    )
    _asdict["BIODOME_COUNT"] = next(
        iter(Items.cur.execute("SELECT count(ROWID) FROM biodome").fetchone().values())
    )
    Items.cur.close()
    Items.conn.close()
    with open("D:/Projects/cmgame/config.json", "w") as cfg_w:
        json.dump(_asdict, cfg_w)


# update_config()
