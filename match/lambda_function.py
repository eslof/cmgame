from enum import unique, Enum, auto
from typing import Dict

from enlist import Enlist
from find import Find
from stop import Stop
from properties import ResponseType, ResponseField
from router import Route, route
from view import View


@unique
class MatchRequest(Enum):
    ENLIST = auto()
    FIND = auto()
    STOP = auto()


routes: Dict[Enum, Route] = {
    MatchRequest.ENLIST: Route(
        handler=Enlist,
        output=lambda value: View.generic(value)
        if type(value) is bool
        else View.response(ResponseType.QUEUE, {ResponseField.Queue.MATCH: value}),
    ),
    MatchRequest.FIND: Route(
        handler=Find,
        output=lambda value: View.response(
            response_type=ResponseType.QUEUE, data={ResponseField.Queue.MATCH: value},
        )
        if value
        else View.generic(False),
    ),
    MatchRequest.STOP: Route(Stop, View.generic),  # Todo: implement
}


@route(routes, MatchRequest)
def lambda_handler(event, context):  # noqa
    pass
