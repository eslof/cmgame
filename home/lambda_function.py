from enum import Enum, unique, auto

from internal import validate_request, assert_inheritance, RequestHandler
from properties import PacketHeader, RequestField, ResponseField, ResponseType, UserAttr
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

    req = validate_request(target=event, request_enum=HomeRequest)
    user_id = User.validate_id(event)

    if req == HomeRequest.NEW:
        user_data = User.get(user_id, f"{UserAttr.HOMES}")
        New.validate(event, len(user_data[UserAttr.HOMES]))
        result = New.run(
            user_id=user_id,
            name=event[RequestField.Home.NAME],
            biodome=event[RequestField.Home.BIODOME],
        )
        return View.generic(result)

    elif req == HomeRequest.SAVE:
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        Save.validate(event)
        result = Save.run(
            home_id=user_data[UserAttr.CURRENT_HOME],
            meta_data=event[RequestField.Home.META],
        )
        return View.generic(result)

    elif req == HomeRequest.GO:
        # TODO: also get home meta data
        user_data = User.get(user_id=user_id, attributes=UserAttr.HOMES)
        Go.validate(event=event, home_count=len(user_data[UserAttr.HOMES]))
        grid = Go.run(
            home_id=user_data[UserAttr.HOMES][event[RequestField.User.HOME_INDEX]]
        )
        return View.construct(
            response_type=ResponseType.HOME_DATA, data={ResponseField.Home.DATA: grid}
        )
    elif req == HomeRequest.DELETE:
        user_data = Delete.validate(event, user_id)
        result = Delete.run(event, user_data, user_id)
        return View.generic(result)
