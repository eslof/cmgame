from database import HomeAttr
from default_imports import *
from router import route, Route

from home.delete import Delete
from home.go import Go
from home.new import New
from home.save import Save


@unique
class HomeRequest(IntEnum):
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
