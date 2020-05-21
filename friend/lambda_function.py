from enum import auto, Enum, unique
from typing import Dict, Any

from friend.add import Add
from friend.invite import Invite
from friend.list import List
from friend.remove import Remove
from properties import ResponseType
from router import Route, route, ROUTES_TYPE
from view import View


@unique
class FriendRequest(Enum):
    ADD = auto()
    INVITE = auto()
    LIST = auto()
    REMOVE = auto()


routes: ROUTES_TYPE = {
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
def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> None:
    pass
