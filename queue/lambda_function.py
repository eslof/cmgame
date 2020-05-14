from enum import Enum, unique, auto

from internal import validate_request, RequestHandler, assert_inheritance, end
from properties import PacketHeader, UserAttr, QueueState
from user import User
from view import View

from .enlist import Enlist
from .find import Find

assert_inheritance([Enlist, Find], RequestHandler)


@unique
class QueueRequest(Enum):
    ENLIST = auto()
    FIND = auto()


def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    validate_request(target=event, request_enum=QueueRequest)
    req = QueueRequest(event[PacketHeader.REQUEST])
    user_id = User.auth(event)

    if req == QueueRequest.ENLIST:
        queue_state = Enlist.validate(user_id)
        Enlist.run(user_id, queue_state)

    elif req == QueueRequest.FIND:
        queue_state = Find.validate(user_id)
        Find.run(user_id, queue_state)

        # TODO: if you find someone we will tell you where to connect the websocket


# breaking up your current matching will be entirely automatic by client closing connection to websocket server
# this triggers setting your queue_state from enlisted or matched to none by the websocket server
