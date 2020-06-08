from typing import no_type_check, List, Union, Dict

from config import Config
from db_properties import UserAttr
from internal import validate_field, end
from helper.item_helper import ItemHelper
from helper.user_helper import UserHelper
from properties import RequestField
from request_handler import RequestHandler
from user_utils import UserUtils


class Accept(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        seed = ItemHelper.itembox_seed(user_id, valid_data[UserAttr.KEY_USED_COUNT])
        item_id = ItemHelper.get_choice_id(
            valid_data[RequestField.ItemBox.CHOICE], seed
        )
        if item_id in valid_data[UserAttr.INVENTORY]:
            results = UserHelper.handle_duplicate_item(user_id)
        else:
            results = UserHelper.handle_new_item(user_id, item_id)
        if not results:
            end("Unable to handle itembox accept.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Union[List[int], int]]:
        validate_field(
            target=event,
            field=RequestField.ItemBox.CHOICE,
            validation=lambda value: type(value) is int
            and 1 <= value <= Config.ITEM_BOX_SIZE,
            message="ItemBox Accept API",
        )
        user_data = UserUtils.get(
            user_id=user_id,
            attributes=f"{UserAttr.INVENTORY}, {UserAttr.KEY_COUNT}, {UserAttr.KEY_USED_COUNT}",
        )
        if not user_data:
            end("Unable to retrieve inventory and current home for user.")
        if user_data[UserAttr.KEY_COUNT] <= 0:
            end("Insufficient keys.")

        return user_data
