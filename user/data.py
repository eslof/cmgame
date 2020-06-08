from typing import Dict, Any, Optional, Union, List, no_type_check

from db_properties import UserAttr
from internal import end
from item_properties import DBItem
from request_handler import RequestHandler
from user_utils import UserUtils
from helper.item_helper import ItemHelper
from helper.user_helper import UserHelper


class Data(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> Dict[str, Any]:
        biodomes: List[DBItem] = ItemHelper.get_biodomes()
        homes: List[DBItem] = valid_data[UserAttr.HOMES]
        inventory: List[DBItem] = ItemHelper.get_inventory(
            valid_data[UserAttr.INVENTORY]
        )
        return UserHelper.template_data(valid_data, homes, inventory, biodomes)

    @staticmethod
    @no_type_check
    def validate(event: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        user_data = UserUtils.get(user_id, UserHelper.data_attributes())
        if not user_data:
            end("Unable to get data attributes for user.")
        return user_data
