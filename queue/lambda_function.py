from default_imports import *
from router import route, Route

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
    QueueRequest.ENLIST: Route(
        handler=Enlist,
        output=lambda value: View.response(
            response_type=ResponseType.QUEUE, data={ResponseField.Queue.MATCH: value},
        )
        if not type(value) is bool
        else View.generic(value),
    ),
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
