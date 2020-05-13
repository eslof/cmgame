from user import User
from view import View
from .enlist import Enlist
from .find import Find
from .end import End

from properties import PacketHeader
from internal import validate_request, RequestHandler, assert_inheritance
from enum import Enum, unique, auto


@unique
class QueueRequest(Enum):
    NONE = auto()
    ENLIST = auto()
    FIND = auto()
    END = auto()


assert_inheritance([Enlist, Find, End], RequestHandler)


def lambda_handler(event, context):
    validate_request(target=event, request_enum=QueueRequest)
    req = QueueRequest(event[PacketHeader.REQUEST])
    user_id = User.auth(event)

    if req == QueueRequest.ENLIST:
        # TODO:implement
        # check user state, already enlisted? update timestamp : new entry
        # unless user is already connected to someone...
        # also surely you should be able to be both enlisted and searching at the same time
        pass

    elif req == QueueRequest.FIND:
        # TODO: implement
        # make sure user isn't already connected? otherwise we don't really care
        # this is where we look for anyone with a 5-10sec old timestamp in enlist table
        # if you find someone we will tell you where to connect the websocket
        pass

    elif req == QueueRequest.END:
        # TODO: implement
        # close your enlisting (aka stop updating your timestamp)
        # breaking up your current matching will be entirely automatic by client closing connection to websocket server
        pass
