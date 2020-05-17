from default_imports import *
from router import route, Route

from .data import Data
from .delete import Delete
from .new import New
from .save import Save

assert_inheritance([Data, Delete, New, Save], RequestHandler)


@unique
class UserRequest(Enum):
    DATA = auto()
    DELETE = auto()
    NEW = auto()
    SAVE = auto()


routes = {
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
    ),
    UserRequest.SAVE: Route(Save, View.generic),
}


@route(routes, UserRequest)
def lambda_handler(event, context):
    pass
