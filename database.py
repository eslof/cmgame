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
    ID = "id"
    BIO = "biodome"
    ITEM = "item"
    QUEUE = "queue"


class ItemAttr:
    BUNDLE = "bundle"
    VERSION = "version"
    NAME = "name"


class QueueAttr:
    DATE = "date"
    STATE = "state"
    USER_ID = "user_id"


class UserAttr:
    SORT_KEY_PREFIX = "U"

    STATE = "state"
    NAME = "name"
    FLAG = "flag"
    META = "meta"
    CURRENT_HOME = "current_home"
    QUEUE_STATE = "queue_state"
    LIST_ID = "match"
    KEY_COUNT = "keys"
    USED_KEY_COUNT = "used_keys"
    INVENTORY_COUNT = "inventory_count"
    INVENTORY = "inventory"
    HOMES = "homes"

    class Home:
        BIODOME = "biodome"
        HOME_ID = "home_id"
        NAME = "name"


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
