# import boto3
# from botocore.exceptions import ClientError
#  dynamodb = boto3.resource('dynamodb')
#  table = dynamodb.Table('staff')
from enum import Enum, unique, auto

# TODO: a lot of stuff here, figure something out

# region Base


class Secret:
    USER_ID = "something random"
    ITEM_BOX_SEED = 133769420


# endregion

# region Game


class Constants:
    ID_TOKEN_BYTE_COUNT = 62

    class User:
        EXPECTED_ID_LENGTH = 42

    class Home:
        SIZE = 49
        NAME_MAX_SIZE = 255

    class Item:
        ID_CHAR_LENGTH = 12


@unique
class Biodome(Enum):
    GRASS = auto()
    DESERT = auto()
    INCA = auto()


# endregion

# region Network


class PacketHeader:
    REQUEST = "request"
    RESPONSE = "response"


class RequestField:
    class Item:
        META = "meta"

    class ItemBox:
        CHOICE = "choice"

    class User:
        META = "meta"
        ITEM_INDEX = "item"
        HOME_INDEX = "home"
        SAVE = "save"
        ID = "id"
        NAME = "name"
        FLAG = "flag"

    class Home:
        META = "meta"
        GRID_INDEX = "grid"
        BIODOME = "biodome"
        NAME = "name"


class ResponseField:
    class Queue:
        MATCH = "match"

    class ItemBox:
        DATA = "data"

    class Generic:
        RESULT = "results"

    class User:
        DATA = "data"
        ID = "id"
        NAME = "name"
        FLAG = "flag"
        HOMES = "homes"
        INVENTORY = "inventory"

    class Item:
        BUNDLE = "name"
        VERSION = "version"

    class Home:
        DATA = "data"
        GRID = "grid"
        NAME = "name"
        BIODOME = "bundle"


# TODO: this being an enum doesn't actually help that much
# TODO: figure out possible down-sides
@unique
class ResponseType(Enum):
    WELCOME = auto()
    GENERIC = auto()
    USER_DATA = auto()
    HOME_DATA = auto()
    ITEM_BOX = auto()
    ITEM_DATA = auto()
    QUEUE = auto()


# endregion

# region Database
@unique
class QueueState(Enum):
    NONE = auto()
    ENLISTED = auto()
    MATCHED = auto()


@unique
class UserState(Enum):
    NEW = auto()
    NORMAL = auto()
    VISITOR = auto()
    BANNED = auto()


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


class UserAttr:
    META = "meta"
    CURRENT_HOME = "current_home"
    NAME = "name"
    STATE = "state"
    QUEUE_STATE = "queue_state"
    FLAG = "flag"
    SELECTED = "selected"
    INVENTORY = "inventory"
    HOME_LIST = "home_count"
    KEY_COUNT = "key_count"
    USED_KEY_COUNT = "used_key_count"
    INVENTORY_COUNT = "inventory_count"


class HomeAttr:
    NAME = "name"
    BIODOME = "biodome"
    META = "meta"
    ITEM_META = "item_meta"
    ITEM_GRID = "item_grid"


# endregion
