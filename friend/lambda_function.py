from default_imports import *
from .add import Add
from .invite import Invite
from .list import List
from .remove import Remove


@unique
class FriendRequest(Enum):
    ADD = auto()
    INVITE = auto()
    LIST = auto()
    REMOVE = auto()


# TODO: Update route output (Callable/default=View.generic)
routes = {
    FriendRequest.ADD: Route(Add, lambda v: None, False),
    FriendRequest.INVITE: Route(
        Invite, lambda v: print(v[PacketHeader.REQUEST]), False
    ),
    FriendRequest.LIST: Route(List, lambda v: None, False),
    FriendRequest.REMOVE: Route(Remove, lambda v: None, False),
}


@route(routes, FriendRequest)
def lambda_handler(event, context):
    pass
