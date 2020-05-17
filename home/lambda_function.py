from properties import HomeAttr
from default_imports import *

from router import *

from .delete import Delete
from .go import Go
from .new import New
from .save import Save

assert_inheritance([Delete, Go, New, Save], RequestHandler)


@unique
class HomeRequest(Enum):
    DELETE = auto()
    GO = auto()
    NEW = auto()
    SAVE = auto()


routes = {
    HomeRequest.DELETE: Route(Delete, View.generic),
    HomeRequest.GO: Route(
        handler=Go,
        output=lambda value: View.response(
            response_type=ResponseType.HOME_DATA,
            data={
                ResponseField.Home.GRID: value[HomeAttr.GRID],
                ResponseField.Home.META: value[HomeAttr.META],
            },
        ),
    ),
    HomeRequest.NEW: Route(New, View.generic),
    HomeRequest.SAVE: Route(Save, View.generic),
}


@route(routes, HomeRequest)
def lambda_handler(event, context):
    pass
