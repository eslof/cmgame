import string
from enum import unique, auto, Enum


# region Game Properties
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


class GameException(Exception):
    pass


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
    REQUEST = "Request"
    RESPONSE = "Response"


class RequestField:
    class Item:
        META = "Meta"

    class ItemBox:
        CHOICE = "Choice"

    class User:
        META = "Meta"
        ITEM = "Item"
        HOME = "Home"
        SAVE = "Save"
        ID = "UserId"
        NAME = "Name"
        FLAG = "Flag"

    class Home:
        META = "Meta"
        GRID = "Grid"
        BIODOME = "Biodome"
        NAME = "Name"


class ResponseField:
    BIODOMES = "Biodomes"

    class Queue:
        MATCH = "Match"

    class ItemBox:
        DATA = "Data"

    class Generic:
        DEBUG = "Debug"
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
