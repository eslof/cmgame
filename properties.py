import string
from enum import unique, auto, Enum
from typing import List


starting_inventory: List[int] = [1, 2, 3, 4]


class GameException(Exception):
    pass


class Constants:
    ID_CHARSET = "".join([string.ascii_letters, string.digits, "-_"])
    ID_GEN_LENGTH = 22
    EXPECTED_ID_LEN = ID_GEN_LENGTH + 1

    class ItemBox:
        ITEM_COUNT = 3

    class User:
        HOME_COUNT_MAX = 5
        META_MAX_LENGTH = 99328
        STARTING_KEY_COUNT = 3
        EXPECTED_ID_LENGTH = 42
        NAME_MAX_LENGTH = 32

    class Home:
        SIZE = 49
        MATCH_GRID_SLOT = 4
        META_MAX_LENGTH = 199680
        NAME_MAX_LENGTH = 32


class ArchiveReason:
    VOLUNTARY = "voluntary"
    BANNED = "banned"
    INACTIVE = "inactive"


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
        ITEM = "item"
        HOME = "home"
        SAVE = "save"
        ID = "id"
        NAME = "name"
        FLAG = "flag"

    class Home:
        META = "meta"
        GRID = "grid"
        BIODOME = "biodome"
        NAME = "name"


class ResponseField:
    class Queue:
        MATCH = "match"

    class ItemBox:
        DATA = "data"

    class Generic:
        DEBUG = "debug"
        ERROR_MESSAGE = "message"
        ERROR_TYPE = "type"
        RESULTS = "results"

    class User:
        WELCOME = "welcome"
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


@unique
class ResponseType(Enum):
    DEBUG = auto()
    ERROR = auto()
    WELCOME = auto()
    GENERIC = auto()
    USER_DATA = auto()
    HOME_DATA = auto()
    ITEM_BOX = auto()
    ITEM_DATA = auto()
    QUEUE = auto()


# endregion
