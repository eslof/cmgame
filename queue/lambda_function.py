from default_imports import *
from internal import end
from database import *

from .enlist import Enlist
from .find import Find
from .stop import Stop

assert_inheritance([Enlist, Find, Stop], RequestHandler)


@unique
class QueueRequest(Enum):
    ENLIST = auto()
    FIND = auto()
    STOP = auto()


# TODO: this could probably be built into a router
def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    req = validate_request(target=event, request_enum=QueueRequest)
    user_id = User.validate_id(event)
    match_server = web_socket_endpoint()
    if not 200 <= match_server["response_code"] <= 299:
        end("Chat server is down")  # TODO: this needs work

    if req == QueueRequest.ENLIST:
        user_data = Enlist.validate(user_id)
        result = Enlist.run(user_data, user_id)
        return View.generic(result)

    elif req == QueueRequest.FIND:
        user_data = Find.validate(user_id)
        listing = Find.run(user_data, user_id)
        # TODO: this needs work probably
        if listing:
            return View.construct(
                response_type=ResponseType.QUEUE,
                data={ResponseField.Queue.MATCH: match_server["address"]},
            )
        else:
            View.generic(False)
    elif req == QueueRequest.STOP:
        user_data = Stop.validate(user_id)
        result = Stop.run(user_data, user_id)
        return View.generic(result)


# breaking up your current matching will be entirely automatic by client closing connection to websocket server
# this triggers setting your queue_state from enlisted or matched to none by the websocket server
