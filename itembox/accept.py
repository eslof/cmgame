from typing import Any, no_type_check, List, Union, Dict

from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr
from internal import validate_field, end
from itembox.helper.user_helper import UserHelper
from properties import RequestField, UserState
from request_handler import RequestHandler
from user_utils import User
from itembox.helper.item_helper import ItemHelper


class Accept(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        seed = ItemHelper.itembox_seed(user_id, valid_data[UserAttr.KEY_USED_COUNT])
        item_id: int = ItemHelper.get_choice(
            valid_data[RequestField.ItemBox.CHOICE], seed
        )
        try:
            if item_id in valid_data[UserAttr.INVENTORY]:
                UserHelper.handle_duplicate_item(user_id)
            else:
                UserHelper.handle_new_item(user_id, item_id)
        except ClientError as e:
            end(e.response["Error"]["Code"])
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Union[List[int], int]]:
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.INVENTORY}, {UserAttr.KEY_COUNT}, {UserAttr.KEY_USED_COUNT}",
        )
        validate_field(
            target=event,
            field=RequestField.ItemBox.CHOICE,
            validation=lambda value: type(value) is int and 1 <= value <= 3,
            message="ItemBox Accept API",
        )
        if user_data[UserAttr.KEY_COUNT] <= 0:
            end(f"Insufficient keys: {user_data[UserAttr.KEY_COUNT]}")

        return user_data
