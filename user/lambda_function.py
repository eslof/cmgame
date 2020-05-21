from default_imports import *

from .data import Data
from .delete import Delete
from .new import New
from .save import Save


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
def lambda_handler(event: Dict[str, Any], context: Dict[str, Any]) -> None:
    pass
