from typing import Dict, no_type_check

from db_properties import UserAttr
from internal import validate_meta, end
from item.helper.home_helper import HomeHelper
from item.helper.internal_helper import InternalHelper
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User


class Update(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        home_id = valid_data[UserAttr.CURRENT_HOME]
        grid_slot = event[RequestField.Home.GRID]
        item_meta = event[RequestField.Item.META]
        if not HomeHelper.update(home_id, grid_slot, item_meta):
            end("Unable to update meta for grid slot.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, str]:
        InternalHelper.validate_grid_request(
            target=event, message="Item Update API (GRID SLOT)"
        )
        validate_meta(
            target=event,
            field=RequestField.Item.META,
            message="Item Update API (META)",
        )
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        if not user_data:
            end("Unable to retrieve current home for user.")
        return user_data
