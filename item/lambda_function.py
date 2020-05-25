from enum import unique, auto, Enum
from typing import Dict

from item.clear import Clear
from item.place import Place
from item.update import Update
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
def lambda_handler(event, context):
    pass
