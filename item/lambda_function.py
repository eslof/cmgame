from enum import Enum, unique, auto

from internal import validate_request, assert_inheritance, RequestHandler
from properties import PacketHeader, UserAttr, RequestField
from user import User
from view import View

from .place import Place
from .update import Update

assert_inheritance([Place, Update], RequestHandler)


@unique
class ItemRequest(Enum):
    PLACE = auto()
    UPDATE = auto()


def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    req = validate_request(target=event, request_enum=ItemRequest)
    user_id = User.validate_id(event)

    if req == ItemRequest.PLACE:
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.INVENTORY_COUNT}, {UserAttr.CURRENT_HOME}",
        )
        Place.validate(event=event, inventory_size=user_data[UserAttr.INVENTORY_COUNT])
        result = Place.run(
            home_id=user_data[UserAttr.CURRENT_HOME],
            item_index=event[RequestField.User.ITEM_INDEX],
            grid_index=event[RequestField.Home.GRID_INDEX],
            item_meta=event[RequestField.Item.META],
        )
        return View.generic(result)

    elif req == ItemRequest.UPDATE:
        user_data = User.get(user_id=user_id, attributes=UserAttr.CURRENT_HOME)
        Update.validate(event)
        result = Update.run(
            home_id=user_data[UserAttr.CURRENT_HOME],
            grid_index=event[RequestField.Home.GRID_INDEX],
            item_meta=event[RequestField.Item.META],
        )
        return View.generic(result)
