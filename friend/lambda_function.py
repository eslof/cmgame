from enum import unique, Enum, auto
from router import route, Route

from friend.add import Add
from friend.invite import Invite
from friend.list import List
from friend.remove import Remove


@unique
class FriendRequest(Enum):
    ADD = auto()
    INVITE = auto()
    LIST = auto()
    REMOVE = auto()


# TODO: Update route output (Callable/default=View.generic)
routes = {
    FriendRequest.ADD: Route(Add, lambda v: None),
    FriendRequest.INVITE: Route(Invite, lambda v: None),
    FriendRequest.LIST: Route(List, lambda v: None),
    FriendRequest.REMOVE: Route(Remove, lambda v: None),
}


@route(routes, FriendRequest)
def lambda_handler(event, context):
    pass
