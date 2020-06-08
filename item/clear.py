from typing import no_type_check, Dict

from db_properties import UserAttr
from internal import end
from helper.home_helper import HomeHelper
from properties import RequestField, Constants
from request_handler import RequestHandler
from user_utils import UserUtils


class Clear(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        home_id = valid_data[UserAttr.CURRENT_HOME]
        grid_slot = event[RequestField.Home.GRID]
        if not HomeHelper.clear_slot(home_id, grid_slot):
            end("Unable to clear grid slot.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, str]:
        HomeHelper.validate_grid_request(event, "Item Clear API (GRID SLOT)")
        if event[RequestField.Home.GRID] == Constants.Home.MATCH_GRID_SLOT:
            end("Cannot clear reserved home grid slot.")
        user_data = UserUtils.get(user_id, UserAttr.CURRENT_HOME)
        if not user_data:
            end("Unable to retrieve current home for user.")
        return user_data
