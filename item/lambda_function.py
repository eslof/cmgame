from default_imports import *
from router import route, Route

from .clear import Clear
from .place import Place
from .update import Update

assert_inheritance([Place, Update], RequestHandler)


@unique
class ItemRequest(Enum):
    PLACE = auto()
    UPDATE = auto()
    CLEAR = auto()


routes = {
    ItemRequest.PLACE: Route(Place, View.generic),
    ItemRequest.UPDATE: Route(Update, View.generic),
    ItemRequest.CLEAR: Route(Clear, View.generic),
}


@route(routes, ItemRequest)
def lambda_handler(event, context):
    pass
