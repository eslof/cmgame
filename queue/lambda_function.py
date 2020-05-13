from user import User
from view import View
from .enlist import Enlist
from .find import Find
from .end import End

from properties import PacketHeader
from internal import sanitize_request, RequestHandler, assert_inheritance
from enum import Enum, unique, auto


@unique
class QueueRequest(Enum):
    NONE = auto()
    ENLIST = auto()
    FIND = auto()
    END = auto()


assert_inheritance([Enlist, Find, End], RequestHandler)


def lambda_handler(event, context):
    sanitize_request(target=event, request_enum=QueueRequest)
    req = QueueRequest(event[PacketHeader.REQUEST])
    user_id = User.auth(event)

    if req == QueueRequest.ENLIST:
        # TODO:implement
        pass

    elif req == QueueRequest.FIND:
        # TODO: implement
        pass

    elif req == QueueRequest.END:
        # TODO: implement
        pass
