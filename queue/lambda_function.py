from user import User
from view import View
from .enlist import Enlist
from .find import Find

from properties import PacketHeader
from internal import validate_request, RequestHandler, assert_inheritance
from enum import Enum, unique, auto


@unique
class QueueRequest(Enum):
    NONE = auto()
    ENLIST = auto()
    FIND = auto()


assert_inheritance([Enlist, Find], RequestHandler)


def lambda_handler(event, context):
    validate_request(target=event, request_enum=QueueRequest)
    req = QueueRequest(event[PacketHeader.REQUEST])
    user_id = User.auth(event)

    if req == QueueRequest.ENLIST:
        # TODO:implement
        # check user state, in match? ignore, shouldn't happen : already enlisted? update timestamp : new entry
        # unless user is already connected to someone...
        # also surely you should be able to be both enlisted and searching at the same time
        pass

    elif req == QueueRequest.FIND:
        # TODO: implement
        # make sure user isn't already connected? otherwise we don't really care
        # this is where we look for anyone with a recent timestamp in enlist table
        # if you find someone we will tell you where to connect the websocket
        pass


# breaking up your current matching will be entirely automatic by client closing connection to websocket server
# this triggers setting your queue_state from enlisted or matched to none by the websocket server

