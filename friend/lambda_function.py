from default_imports import *
from router import *

from .add import Add
from .invite import Invite
from .list import List
from .remove import Remove

assert_inheritance([Add, Invite, List, Remove], RequestHandler)


@unique
class FriendRequest(Enum):
    ADD = auto()
    INVITE = auto()
    LIST = auto()
    REMOVE = auto()


# TODO: Update route output (Callable/default=View.generic)
routes = {
    FriendRequest.ADD: Route(Add, View.generic),
    FriendRequest.INVITE: Route(Invite, View.generic),
    FriendRequest.LIST: Route(List, View.generic),
    FriendRequest.REMOVE: Route(Remove, View.generic),
}


@route(routes, FriendRequest)
def lambda_handler(event, context):
    pass
