from user import User
from view import View
from .place import Place
from .update import Update

from properties import PacketHeader, UserAttr, RequestField
from internal import validate_request, assert_inheritance, RequestHandler
from enum import Enum, unique, auto


@unique
class ItemRequest(Enum):
    PLACE = auto()
    UPDATE = auto()


assert_inheritance([Place, Update], RequestHandler)


def lambda_handler(event, context):
    validate_request(target=event, request_enum=ItemRequest)
    req = ItemRequest(event[PacketHeader.REQUEST])

    user_id = User.auth(event)

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
