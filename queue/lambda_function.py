from user import User
from view import View
from .enlist import Enlist
from .find import Find
from .end import End

from properties import PacketHeader
from internal import sanitize_request
from enum import Enum, unique, auto


@unique
class QueueRequest(Enum):
    NONE = auto()
    ENLIST = auto()
    FIND = auto()
    END = auto()


def lambda_handler(event, context):
    sanitize_request(target=event, request_enum=QueueRequest)
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
