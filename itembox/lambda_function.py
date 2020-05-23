from enum import Enum, auto, unique
from typing import Dict, Any

from database import ItemAttr
from itembox.accept import Accept
from itembox.demand import Demand
from properties import ResponseType, ResponseField
from router import ROUTES_TYPE, Route, route
from view import View


@unique
class ItemBoxRequest(Enum):
    ACCEPT = auto()
    DEMAND = auto()


routes: Dict[Enum, Route] = {
    ItemBoxRequest.ACCEPT: Route(
        handler=Accept,
        output=lambda value: View.response(
            response_type=ResponseType.ITEM_DATA,
            data={
                ResponseField.Item.BUNDLE: value[ItemAttr.BUNDLE],
                ResponseField.Item.VERSION: value[ItemAttr.VERSION],
            },
        ),
    ),
    ItemBoxRequest.DEMAND: Route(
        handler=Demand,
        output=lambda value: View.response(
            response_type=ResponseType.ITEM_BOX,
            data={ResponseField.ItemBox.DATA: value},
        ),
    ),
}


@route(routes, ItemBoxRequest)
def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    pass
