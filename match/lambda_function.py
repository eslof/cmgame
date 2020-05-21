from default_imports import *
from match.enlist import Enlist
from match.find import Find
from match.stop import Stop
from router import route, Route


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
