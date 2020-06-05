from typing import Dict, List, no_type_check, Union

from db_properties import UserAttr
from internal import end
from item_factory import DBItem
from request_handler import RequestHandler
from user_utils import User
from .helper.item_helper import ItemHelper


class Demand(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> List[DBItem]:
        seed = ItemHelper.itembox_seed(user_id, valid_data[UserAttr.KEY_USED_COUNT])
        return ItemHelper.get_itembox(seed)

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Union[List[str], int]]:
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.KEY_COUNT}, {UserAttr.KEY_USED_COUNT}",
        )
        if not user_data:
            end("Unable to retrieve key and used key count for user.")
        if user_data[UserAttr.KEY_COUNT] <= 0:
            end(f"Insufficient keys: {user_data[UserAttr.KEY_COUNT]}")

        return user_data
