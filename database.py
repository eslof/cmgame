from typing import Dict, Union

import boto3

from item_factory import BUNDLE, VERSION


# TODO: create cloudfront distributed s3 bucket for config data like ws url
def web_socket_endpoint() -> Dict[str, Union[str, int]]:
    #  TODO: get live state
    return {"response_code": 200, "address": "domain.com/ws"}


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cmgame")


class ItemAttr:
    BUNDLE = BUNDLE
    VERSION = VERSION


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


class MatchAttr:
    DATE = "date"
    LISTER_ID = "lister_id"
    FINDER_ID = "finder_id"
