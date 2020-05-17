from default_imports import *
from router import *

from .place import Place
from .update import Update

assert_inheritance([Place, Update], RequestHandler)


@unique
class ItemRequest(Enum):
    PLACE = auto()
    UPDATE = auto()


routes = {
    ItemRequest.PLACE: Route(Place, View.generic),
    ItemRequest.UPDATE: Route(Update, View.generic),
}


@route(routes, ItemRequest)
def lambda_handler(event, context):
    pass
