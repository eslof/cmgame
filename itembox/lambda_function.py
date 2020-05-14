from enum import Enum, unique, auto

# TODO: figure out a prettier way, black forces line split for each class
from properties import PacketHeader, RequestField, ResponseField, ResponseType
from properties import UserAttr, ItemAttr
from internal import validate_request, RequestHandler, assert_inheritance
from user import User
from view import View

from .accept import Accept
from .demand import Demand

assert_inheritance([Demand, Accept], RequestHandler)


@unique
class ItemBoxRequest(Enum):
    DEMAND = auto()
    ACCEPT = auto()


def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    validate_request(target=event, request_enum=ItemBoxRequest)
    req = ItemBoxRequest(event[PacketHeader.REQUEST])
    user_id = User.validate_id(event)

    if req == ItemBoxRequest.DEMAND:
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.KEY_COUNT}, {UserAttr.INVENTORY}, {UserAttr.USED_KEY_COUNT}",
        )
        # TODO: maybe we do the db request in the validation?
        Demand.validate(user_data[UserAttr.KEY_COUNT])

        # unique for user; different every time
        # if user_id is random and not known by user it should be predictable by only ourselves
        # TODO: verify that user cannot predict + if it even makes any difference
        seed = user_id + user_data[UserAttr.USED_KEY_COUNT]

        item_box_data = Demand.run(inventory=user_data[UserAttr.INVENTORY], seed=seed)
        return View.construct(
            response_type=ResponseType.ITEM_BOX,
            data={ResponseField.ItemBox.DATA: item_box_data},
        )

    elif req == ItemBoxRequest.ACCEPT:
        Accept.validate(event)
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
