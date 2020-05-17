from default_imports import *
from router import *

from .enlist import Enlist
from .find import Find
from .stop import Stop

assert_inheritance([Enlist, Find, Stop], RequestHandler)


@unique
class QueueRequest(Enum):
    ENLIST = auto()
    FIND = auto()
    STOP = auto()


routes = {
    QueueRequest.ENLIST: Route(Enlist, View.generic),
    QueueRequest.FIND: Route(
        handler=Find,
        output=lambda value: View.response(
            response_type=ResponseType.QUEUE, data={ResponseField.Queue.MATCH: value},
        )
        if value
        else View.generic(False),
    ),
    QueueRequest.STOP: Route(Stop, View.generic),
}


@route(routes, QueueRequest)
def lambda_handler(event, context):
    pass
