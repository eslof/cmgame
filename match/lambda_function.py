from default_imports import *
from .enlist import Enlist
from .find import Find
from .stop import Stop


@unique
class MatchRequest(Enum):
    ENLIST = auto()
    FIND = auto()
    STOP = auto()


routes = {
    MatchRequest.ENLIST: Route(
        handler=Enlist,
        output=lambda value: View.response(
            response_type=ResponseType.QUEUE, data={ResponseField.Queue.MATCH: value},
        )
        if not type(value) is bool
        else View.generic(value),
    ),
    MatchRequest.FIND: Route(
        handler=Find,
        output=lambda value: View.response(
            response_type=ResponseType.QUEUE, data={ResponseField.Queue.MATCH: value},
        )
        if value
        else View.generic(False),
    ),
    MatchRequest.STOP: Route(Stop, View.generic),
}


@route(routes, MatchRequest)
def lambda_handler(event, context):
    pass
