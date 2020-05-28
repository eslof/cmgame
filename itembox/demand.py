from typing import Any, Dict, List, no_type_check, Union

from database import UserAttr
from internal import end
from request_handler import RequestHandler
from user_utils import User
from .helper.item_helper import ItemHelper


class Demand(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> List[Dict[str, Any]]:
        inventory = valid_data[UserAttr.INVENTORY]
        seed = ItemHelper.itembox_seed(
            user_id, valid_data[UserAttr.KEY_COUNT], valid_data[UserAttr.KEY_USED_COUNT]
        )
        return ItemHelper.itembox(3, seed, inventory)

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Union[List[str], int]]:
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.KEY_COUNT}, {UserAttr.KEY_USED_COUNT}",
        )
        if user_data[UserAttr.KEY_COUNT] <= 0:
            end(f"Insufficient keys: {user_data[UserAttr.KEY_COUNT]}")

        return user_data
