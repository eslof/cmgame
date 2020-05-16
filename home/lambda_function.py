from enum import Enum, unique, auto

from request_handler import RequestHandler
from internal import validate_request, assert_inheritance
from properties import RequestField, ResponseField, ResponseType, UserAttr
from user import User
from view import View

from .delete import Delete
from .go import Go
from .new import New
from .save import Save

assert_inheritance([Delete, Go, New, Save], RequestHandler)


@unique
class HomeRequest(Enum):
    NEW = auto()
    SAVE = auto()
    GO = auto()
    DELETE = auto()


def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    req = validate_request(event, HomeRequest)
    user_id = User.validate_id(event)

    if req == HomeRequest.NEW:
        user_data = User.get(user_id, UserAttr.HOMES)
        New.validate(event, user_data)
        result = New.run(event, user_id)
        return View.generic(result)

    elif req == HomeRequest.SAVE:
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        Save.validate(event)
        result = Save.run(event, user_data)
        return View.generic(result)

    elif req == HomeRequest.GO:
        # TODO: also get home meta data
        user_data = User.get(user_id, UserAttr.HOMES)
        Go.validate(event, user_data)
        grid = Go.run(event, user_data)
        return View.construct(
            response_type=ResponseType.HOME_DATA, data={ResponseField.Home.DATA: grid}
        )
    elif req == HomeRequest.DELETE:
        user_data = Delete.validate(event, user_id)
        result = Delete.run(event, user_data, user_id)
        return View.generic(result)
