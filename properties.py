# import boto3
# from botocore.exceptions import ClientError
#  dynamodb = boto3.resource('dynamodb')
#  table = dynamodb.Table('staff')
from enum import Enum, unique, auto

# TODO: a lot of stuff here, figure something out

# region Base
from typing import Union


class Secret:
    USER_ID = "something random"
    ITEMBOX = 133769420


# endregion

# region Game


starting_inventory = [
    "q1H7AD0zllObeidAEwvui",
    "eMg5ltDhJ7Yy3jhjG6Svt",
    "D4JlrGOb_wNdNgj16vv_d",
    "1-Zlb-R0OGLfmqbBpSwL2",
]


class Constants:
    ID_TOKEN_BYTE_COUNT = 62

    class User:
        HOME_COUNT_MAX = 5
        META_MAX_LENGTH = 1024
        STARTING_KEY_COUNT = 3
        EXPECTED_ID_LENGTH = 42
        NAME_MAX_LENGTH = 128

    class Home:
        SIZE = 49
        NAME_MAX_LENGTH = 255

    class Item:
        ID_CHAR_LENGTH = 12


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
        META = "meta"
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
        META = "meta"
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
    NAME = "name"
    BIODOME = "biodome"
    META = "meta"
    GRID = "grid"

    class Grid:
        ITEM = "item"
        META = "meta"


# endregion
