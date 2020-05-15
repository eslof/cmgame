from enum import Enum, unique, auto

from internal import validate_request, RequestHandler, assert_inheritance
from properties import PacketHeader, RequestField, ResponseType, ResponseField
from user import User
from view import View

from .new import New
from .data import Data
from .save import Save

assert_inheritance([New, Data, Save], RequestHandler)


@unique
class UserRequest(Enum):
    NEW = auto()
    DATA = auto()
    SAVE = auto()


def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    req = validate_request(target=event, request_enum=UserRequest)

    if req == UserRequest.NEW:
        New.validate(event)
        encrypted_uuid = New.run(
            name=event[RequestField.User.NAME], flag=event[RequestField.User.FLAG]
        )
        return View.construct(
            response_type=ResponseType.WELCOME,
            data={ResponseField.User.ID: encrypted_uuid},
        )

    user_id = User.validate_id(event)

    if req == UserRequest.DATA:
        user_data = Data.run(user_id)
        return View.construct(
            response_type=ResponseType.WELCOME,
            data={ResponseField.User.DATA: user_data},
        )

    elif req == UserRequest.SAVE:
        save_request = Save.validate(event)
        result = Save.run(request=save_request, user_id=user_id, event=event)
        return View.generic(result)
