from user import User
from view import View
from .enlist import Enlist
from .find import Find

from properties import PacketHeader, UserAttr, QueueState
from internal import validate_request, RequestHandler, assert_inheritance, end
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
    queue_state = QueueState(
        User.get(user_id=user_id, attributes=f"{UserAttr.QUEUE_STATE}")
    )
    if queue_state == QueueState.MATCHED:
        end("Queue request API (ENLIST): Already matched.")

    if req == QueueRequest.ENLIST:
        if queue_state == QueueState.ENLISTED:
            # TODO: update current listing with new timestamp
            pass
        elif queue_state == QueueState.NONE:
            # TODO: create new listing
            pass

    elif req == QueueRequest.FIND:
        # TODO: look for enlisted other
        if queue_state == QueueState.ENLISTED:
            # TODO: AND update current listing with new timestamp
            pass

        # TODO: if you find someone we will tell you where to connect the websocket


# breaking up your current matching will be entirely automatic by client closing connection to websocket server
# this triggers setting your queue_state from enlisted or matched to none by the websocket server

