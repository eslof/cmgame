from typing import Dict, Union

import boto3


# TODO: create cloudfront distributed s3 bucket for config data like ws url
def web_socket_endpoint() -> Dict[str, Union[str, int]]:
    #  TODO: get live state
    return {"response_code": 200, "address": "domain.com/ws"}


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cmgame")

# TODO: look into this
"""
from typing import TypedDict


class WelcomePacket():
    name: user_data[UserAttr.NAME],
    flag: user_data[UserAttr.FLAG],
    meta: user_data[UserAttr.META],
    homes: homes,
    inventory: inventory,

class Item(TypedDict):
    bundle: str
    version: int


class GridSlot(TypedDict):
    item: int
    meta: str


class Home(TypedDict):
    meta: str
    grid: Dict[str, GridSlot]
"""


class UserAttr:
    SORT_KEY_PREFIX = "U"

    STATE = "state"
    NAME = "name"
    FLAG = "flag"
    META = "meta"
    MATCH_ID = "match_id"
    CURRENT_HOME = "current_home"
    HOMES = "homes"
    HOME_COUNT = "home_count"
    KEY_COUNT = "keys"
    KEY_USED_COUNT = "used_keys"
    INVENTORY = "inventory"
    INVENTORY_COUNT = "inventory_count"

    class Home:
        ID = "id"
        NAME = "name"
        BIODOME = "biodome"


class HomeAttr:
    SORT_KEY_PREFIX = "H"
    MATCH_GRID_SLOT = "4"

    NAME = "name"
    BIODOME = "biodome"
    META = "meta"
    GRID = "grid"
    GRID_SLOT = "grid_slot"

    class GridSlot:
        ITEM = "item"
        META = "meta"


META_SIZE_LIMIT: Dict[str, int] = {
    UserAttr.META: 2048,
    HomeAttr.META: 2048,
    HomeAttr.GridSlot.META: 1024,
}


class TableKey:
    PARTITION = "type"
    SORT = "id"


class TablePartition:
    USER = "user"
    HOME = "home"
    MATCH = "queue"


class ItemAttr:
    BUNDLE = "bundle"
    VERSION = "version"


class MatchAttr:
    DATE = "date"
    LISTER_ID = "lister_id"
    FINDER_ID = "finder_id"
