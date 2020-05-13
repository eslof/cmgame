from user import User
from view import View
from .new import New
from .save import Save
from .go import Go

from internal import sanitize_field, sanitize_request
from enum import Enum, unique, auto
from properties import (
    PacketHeader,
    RequestField,
    ResponseType,
    ResponseField,
    UserAttr,
)


@unique
class HomeRequests(Enum):
    NEW = auto()
    SAVE = auto()
    GO = auto()


def lambda_handler(event, context):
    sanitize_request(target=event, request_enum=HomeRequests)
    req = HomeRequests(event[PacketHeader.REQUEST])
    user_id = User.auth(event)

    if req == HomeRequests.NEW:
        New.sanitize(event)
        result = New.run(
            user_id=user_id,
            name=event[RequestField.Home.NAME],
            biodome=event[RequestField.Home.BIODOME],
        )
        return View.generic(result)

    elif req == HomeRequests.SAVE:
        user_data = User.get(user_id=user_id, attributes=UserAttr.CURRENT_HOME)
        Save.sanitize(event)
        result = Save.run(
            home_id=user_data[UserAttr.CURRENT_HOME],
            meta_data=event[RequestField.Home.META],
        )
        return View.generic(result)

    elif req == HomeRequests.GO:
        # TODO: also get home meta data
        user_data = User.get(user_id=user_id, attributes=UserAttr.HOME_LIST)
        Go.sanitize(event=event, home_count=len(user_data[UserAttr.HOME_LIST]))
        grid = Go.run(
            home_id=user_data[UserAttr.HOME_LIST][event[RequestField.User.HOME_INDEX]]
        )
        return View.construct(
            response_type=ResponseType.HOME_DATA, data={ResponseField.Home.DATA: grid}
        )
