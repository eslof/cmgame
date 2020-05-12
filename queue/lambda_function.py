from user import User
from view import View
from .enlist import Enlist
from .find import Find
from .end import End

from properties import PacketHeader
from internal import sanitize_field
from enum import Enum, unique, auto


@unique
class QueueRequest(Enum):
    NONE = auto()
    ENLIST = auto()
    FIND = auto()
    END = auto()


def lambda_handler(event, context):
    sanitize_field(
        target=event,
        field=PacketHeader.REQUEST,
        sanity=lambda value: isinstance(value, int)
        and value in QueueRequest._value2member_map_
        and QueueRequest(value) != QueueRequest.NONE,
        sanity_id="Queue Request API",
    )

    user_id = User.auth(event)
    req = QueueRequest(event[PacketHeader.REQUEST])

    if req == QueueRequest.ENLIST:
        # TODO:implement
        pass

    elif req == QueueRequest.FIND:
        # TODO: implement
        pass

    elif req == QueueRequest.END:
        # TODO: implement
        pass
