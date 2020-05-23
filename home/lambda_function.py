from enum import auto, unique, Enum
from typing import Dict, Any

from database import HomeAttr
from home.delete import Delete
from home.go import Go
from home.new import New
from home.save import Save
from properties import ResponseField, ResponseType
from router import route, Route, ROUTES_TYPE
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
def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    pass
