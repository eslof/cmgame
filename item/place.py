from typing import no_type_check, Union, Dict

from config import Config
from db_properties import UserAttr
from internal import validate_meta, end, validate_choice
from helper.home_helper import HomeHelper
from properties import RequestField, Constants
from request_handler import RequestHandler
from user_utils import UserUtils


class Place(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        if not HomeHelper.set_slot(
            home_id=valid_data[UserAttr.CURRENT_HOME],
            grid_slot=str(event[RequestField.Home.GRID]),
            item=event[RequestField.User.ITEM],
            meta=event[RequestField.Item.META],
        ):
            end("Unable to update selected grid slot.")

        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Union[int, str]]:
        HomeHelper.validate_grid_request(event, "Item Place API (GRID SLOT)")
        if event[RequestField.Home.GRID] == Constants.Home.MATCH_GRID_SLOT:
            end("Cannot place reserved home grid slot.")
        validate_meta(
            target=event,
            field=RequestField.Item.META,
            max_size=Config.GRID_META_LIMIT,
            message="Item Place API (META)",
        )
        user_data = UserUtils.get(
            user_id, f"{UserAttr.INVENTORY_COUNT}, {UserAttr.CURRENT_HOME}",
        )
        if not user_data:
            end("Unable to retrieve inventory and current home for user.")
        validate_choice(
            target=event,
            field=RequestField.User.ITEM,
            max=user_data[UserAttr.INVENTORY_COUNT],
            message="Item Place API (ITEM CHOICE)",
        )
        return user_data
