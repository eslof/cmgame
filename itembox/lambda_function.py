from enum import Enum, auto, unique
from typing import Dict

from item_factory import ItemAttr
from itembox.accept import Accept
from itembox.demand import Demand
from properties import ResponseType, ResponseField
from router import Route, route
from view import View


@unique
class ItemBoxRequest(Enum):
    ACCEPT = auto()
    DEMAND = auto()


# TODO: system under rework
routes: Dict[Enum, Route] = {
    ItemBoxRequest.ACCEPT: Route(
        handler=Accept, output=lambda value: View.generic(True),
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
def lambda_handler(event, context):
    pass
