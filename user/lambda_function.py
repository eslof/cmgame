from user import User
from view import View
from .new import New
from .data import Data
from .save import Save

from properties import PacketHeader, RequestField, ResponseType, ResponseField
from internal import validate_request, RequestHandler, assert_inheritance
from enum import Enum, unique, auto


@unique
class UserRequest(Enum):
    NEW = auto()
    DATA = auto()
    SAVE = auto()


assert_inheritance([New, Data, Save], RequestHandler)


def lambda_handler(event, context):
    validate_request(target=event, request_enum=UserRequest)
    req = UserRequest(event[PacketHeader.REQUEST])

    if req == UserRequest.NEW:
        New.validate(event)
        encrypted_uuid = New.run(
            name=event[RequestField.User.NAME], flag=event[RequestField.User.FLAG]
        )
        return View.construct(
            response_type=ResponseType.WELCOME,
            data={ResponseField.User.ID: encrypted_uuid},
        )

    user_id = User.auth(event)

    if req == UserRequest.DATA:
        user_data = Data.run(user_id)
        return View.construct(
            response_type=ResponseType.WELCOME,
            data={ResponseField.User.DATA: user_data},
        )

    elif req == UserRequest.SAVE:
        Save.validate(event)
        result = Save.run(
            save_request=event[RequestField.User.SAVE], user_id=user_id, event=event
        )
        return View.generic(result)
