import string
from enum import unique, auto, Enum


# region Game Properties
class GameException(Exception):
    pass


class Constants:
    ID_CHARSET = "".join([string.ascii_letters, string.digits, "-_"])
    ID_GEN_LENGTH = 22
    EXPECTED_ID_LEN = ID_GEN_LENGTH + 1

    class User:
        NAME_MAX_LENGTH = 32

    class Home:
        SIZE = 49
        MATCH_GRID_SLOT = 4
        NAME_MAX_LENGTH = 32


# endregion
# region Network Packet Definitions
@unique
class ResponseType(Enum):
    DEBUG = auto()
    ERROR = auto()
    GENERIC = auto()
    NEW = auto()
    USER_DATA = auto()
    HOME_DATA = auto()
    ITEM_BOX = auto()
    ITEM_DATA = auto()
    QUEUE = auto()


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
    BIODOMES = "Biodomes"

    class Queue:
        MATCH = "match"

    class ItemBox:
        DATA = "data"

    class Generic:
        DEBUG = "debug"
        RESULTS = "Results"

        class Error:
            MESSAGE = "Message"
            TYPE = "Type"

    class User:
        KEYS = "Keys"
        WELCOME = "Welcome"
        META = "Meta"
        DATA = "Data"
        ID = "UserId"
        NAME = "Name"
        FLAG = "Flag"
        HOMES = "Homes"
        INVENTORY = "Inventory"

    class Item:
        BUNDLE = "Name"
        VERSION = "Version"

    class Home:
        META = "Meta"
        GRID = "Grid"
        NAME = "Name"
        BIODOME = "Bundle"


# endregion
