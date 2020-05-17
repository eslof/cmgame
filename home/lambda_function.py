from enum import Enum, unique, auto

from request_handler import RequestHandler
from internal import validate_request, assert_inheritance
from properties import ResponseField, ResponseType, HomeAttr
from router import Router, Route
from user import User
from view import View

from .delete import Delete
from .go import Go
from .new import New
from .save import Save

assert_inheritance([Delete, Go, New, Save], RequestHandler)


@unique
class HomeRequest(Enum):
    DELETE = auto()
    GO = auto()
    NEW = auto()
    SAVE = auto()


routes = {
    HomeRequest.DELETE: Route(Delete, View.generic),
    HomeRequest.GO: Route(
        handler=Delete,
        output=lambda value: View.construct(
            response_type=ResponseType.HOME_DATA,
            data={
                ResponseField.Home.GRID: value[HomeAttr.GRID],
                ResponseField.Home.META: value[HomeAttr.META],
            },
        ),
    ),
    HomeRequest.NEW: Route(Delete, View.generic),
    HomeRequest.SAVE: Route(Delete, View.generic),
}


def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    req = validate_request(event, HomeRequest)
    user_id = User.validate_id(event)
    Router.handle(routes[req], event, user_id)
