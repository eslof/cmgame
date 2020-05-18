from enum import Enum, unique, auto

# TODO: a lot of stuff here, figure something out

# region Base


class Seed:
    USER_ID = 677983735
    ITEMBOX = 232837927


# endregion

# region Game


starting_inventory = [
    "q1H7AD0zllObeidAEwvui",
    "eMg5ltDhJ7Yy3jhjG6Svt",
    "D4JlrGOb_wNdNgj16vv_d",
    "1-Zlb-R0OGLfmqbBpSwL2",
]


class Constants:
    ID_GEN_LENGTH = 22
    # Certain partitions have 1 char prefix added (U for User, H for Home)
    EXPECTED_ID_LEN = ID_GEN_LENGTH + 1

    class User:
        HOME_COUNT_MAX = 5
        META_MAX_LENGTH = 99328
        STARTING_KEY_COUNT = 3
        EXPECTED_ID_LENGTH = 42
        NAME_MAX_LENGTH = 32

    class Home:
        SIZE = 49
        META_MAX_LENGTH = 199680
        NAME_MAX_LENGTH = 32


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
        ERROR = "error"
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
    ERROR = auto()
    WELCOME = auto()
    GENERIC = auto()
    USER_DATA = auto()
    HOME_DATA = auto()
    ITEM_BOX = auto()
    ITEM_DATA = auto()
    QUEUE = auto()


# endregion
