from user import User
from view import View
from .demand import Demand
from .accept import Accept

from properties import (
    PacketHeader,
    UserAttr,
    ResponseType,
    ResponseField,
    RequestField,
    ItemAttr,
)
from internal import sanitize_request
from enum import Enum, unique, auto


@unique
class ItemBoxRequest(Enum):
    NONE = auto()
    DEMAND = auto()
    ACCEPT = auto()


def lambda_handler(event, context):
    sanitize_request(target=event, request_enum=ItemBoxRequest)
    req = ItemBoxRequest(event[PacketHeader.REQUEST])

    user_id = User.auth(event)

    if req == ItemBoxRequest.DEMAND:
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.KEY_COUNT}, {UserAttr.INVENTORY}, {UserAttr.USED_KEY_COUNT}",
        )
        Demand.sanitize(user_data[UserAttr.KEY_COUNT])

        # unique for user; different every time
        seed = user_id + user_data[UserAttr.USED_KEY_COUNT]

        item_box_data = Demand.run(inventory=user_data[UserAttr.INVENTORY], seed=seed)
        return View.construct(
            response_type=ResponseType.ITEM_BOX,
            data={ResponseField.ItemBox.DATA: item_box_data},
        )

    elif req == ItemBoxRequest.ACCEPT:
        Accept.sanitize(event)
        item_data = Accept.run(
            user_id=user_id, choice=event[RequestField.ItemBox.CHOICE]
        )
        return View.construct(
            response_type=ResponseType.ITEM_DATA,
            data={
                ResponseField.Item.BUNDLE: item_data[ItemAttr.BUNDLE],
                ResponseField.Item.VERSION: item_data[ItemAttr.VERSION],
            },
        )
