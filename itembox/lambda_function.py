from database import ItemAttr
from default_imports import *
from itembox.accept import Accept
from itembox.demand import Demand


@unique
class ItemBoxRequest(Enum):
    ACCEPT = auto()
    DEMAND = auto()


routes = {
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
def lambda_handler(event, context):
    pass
