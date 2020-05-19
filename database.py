import boto3


# TODO: create cloudfront distributed s3 bucket for config data like ws url
def web_socket_endpoint():
    #  TODO: get live state
    return {"response_code": 200, "address": "domain.com/ws"}


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cmgame")

# region Database


class TableKey:
    PARTITION = "type"
    SORT = "id"


class TablePartition:
    USER = "user"
    HOME = "home"
    QUEUE = "queue"


class ItemAttr:
    BUNDLE = "bundle"
    VERSION = "version"


class QueueAttr:
    DATE = "date"
    STATE = "state"
    LISTER_ID = "lister_id"
    FINDER_ID = "finder_id"


class UserAttr:
    SORT_KEY_PREFIX = "U"

    STATE = "state"
    NAME = "name"
    FLAG = "flag"
    META = "meta"
    QUEUE_ID = "queue_id"
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

    NAME = "name"
    BIODOME = "biodome"
    META = "meta"
    GRID = "grid"

    class Grid:
        ITEM = "item"
        META = "meta"


# endregion
