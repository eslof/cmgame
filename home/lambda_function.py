from user import User
from view import View
from .new import New
from .save import Save
from .go import Go

from internal import sanitize_request
from enum import Enum, unique, auto
from properties import (
    PacketHeader,
    RequestField,
    ResponseType,
    ResponseField,
    UserAttr,
)


@unique
class HomeRequest(Enum):
    NEW = auto()
    SAVE = auto()
    GO = auto()


def lambda_handler(event, context):
    sanitize_request(target=event, request_enum=HomeRequest)
    req = HomeRequest(event[PacketHeader.REQUEST])
    user_id = User.auth(event)

    if req == HomeRequest.NEW:
        New.sanitize(event)
        result = New.run(
            user_id=user_id,
            name=event[RequestField.Home.NAME],
            biodome=event[RequestField.Home.BIODOME],
        )
        return View.generic(result)

    elif req == HomeRequest.SAVE:
        user_data = User.get(user_id=user_id, attributes=UserAttr.CURRENT_HOME)
        Save.sanitize(event)
        result = Save.run(
            home_id=user_data[UserAttr.CURRENT_HOME],
            meta_data=event[RequestField.Home.META],
        )
        return View.generic(result)

    elif req == HomeRequest.GO:
        # TODO: also get home meta data
        user_data = User.get(user_id=user_id, attributes=UserAttr.HOME_LIST)
        Go.sanitize(event=event, home_count=len(user_data[UserAttr.HOME_LIST]))
        grid = Go.run(
            home_id=user_data[UserAttr.HOME_LIST][event[RequestField.User.HOME_INDEX]]
        )
        return View.construct(
            response_type=ResponseType.HOME_DATA, data={ResponseField.Home.DATA: grid}
        )
