from enum import unique, auto, Enum
from typing import Dict

from clear import Clear
from place import Place
from update import Update
from router import route, Route
from view import View


@unique
class ItemRequest(Enum):
    PLACE = auto()
    UPDATE = auto()
    CLEAR = auto()


routes: Dict[Enum, Route] = {
    ItemRequest.PLACE: Route(Place, View.generic),
    ItemRequest.UPDATE: Route(Update, View.generic),
    ItemRequest.CLEAR: Route(Clear, View.generic),
}


@route(routes, ItemRequest)
def lambda_handler(event, context):  # noqa
    pass
