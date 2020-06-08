from enum import auto, unique, Enum
from typing import Dict

from db_properties import HomeAttr
from delete import Delete
from go import Go
from new import New
from save import Save
from properties import ResponseField, ResponseType
from router import route, Route
from view import View


@unique
class HomeRequest(Enum):
    DELETE = auto()
    GO = auto()
    NEW = auto()
    SAVE = auto()


routes: Dict[Enum, Route] = {
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
def lambda_handler(event, context):  # noqa
    pass
