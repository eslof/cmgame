from default_imports import *
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
    FriendRequest.ADD: Route(
        Add, lambda value: View.response(ResponseType.DEBUG, value), False
    ),
    FriendRequest.INVITE: Route(
        Invite, lambda value: View.response(ResponseType.DEBUG, value), False
    ),
    FriendRequest.LIST: Route(
        List, lambda value: View.response(ResponseType.DEBUG, value), False
    ),
    FriendRequest.REMOVE: Route(
        Remove, lambda value: View.response(ResponseType.DEBUG, value), False
    ),
}


@route(routes, FriendRequest)
def lambda_handler(event, context):
    pass
