class RateException(Exception):
    pass


class AWSError:
    WCU_LIMIT = "ProvisionedThroughputExceededException"
    REQ_LIMIT = "RequestLimitExceeded"
    RATE_LIMIT = "ThrottlingException"
    CONDITIONAL = "ConditionalCheckFailedException"


class UserAttr:
    SORT_KEY_PREFIX = "U"

    STATE = "state"
    NAME = "name"
    FLAG = "flag"
    META = "meta"
    MATCH_ID = "match_id"
    LIST_ID = "list_id"
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
    MATCH_GRID_SLOT = 4

    NAME = "name"
    BIODOME = "biodome"
    META = "meta"
    GRID = "grid"
    GRID_SLOT = "grid_slot"

    class GridSlot:
        ITEM = "item"
        META = "meta"


class ArchiveAttr(UserAttr):
    ARCHIVE_REASON = "archive_reason"


class TableKey:
    PARTITION = "type"
    SORT = "id"


class TablePartition:
    USER_ARCHIVE = "user_archive"
    USER = "user"
    HOME = "home"
    MATCH = "queue"


class MatchAttr:
    LISTER_ID = "lister_id"
    FINDER_ID = "finder_id"
