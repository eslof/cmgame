from enum import Enum, auto, unique
from typing import Any, Dict

from properties import ResponseType, ResponseField
from router import Route, ROUTES_TYPE, route
from user.data import Data
from user.delete import Delete
from user.new import New
from user.save import Save
from view import View


@unique
class UserRequest(Enum):
    DATA = auto()
    DELETE = auto()
    NEW = auto()
    SAVE = auto()


routes: ROUTES_TYPE = {
    UserRequest.DATA: Route(
        handler=Data,
        output=lambda value: View.response(
            response_type=ResponseType.USER_DATA, data={ResponseField.User.DATA: value},
        ),
    ),
    UserRequest.DELETE: Route(Delete, View.generic),
    UserRequest.NEW: Route(
        handler=New,
        output=lambda value: View.response(
            response_type=ResponseType.WELCOME, data={ResponseField.User.ID: value},
        ),
        require_id=False,
    ),
    UserRequest.SAVE: Route(Save, View.generic),
}


@route(routes, UserRequest)
def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    pass
