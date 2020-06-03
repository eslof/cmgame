from typing import no_type_check, Dict

from database import table
from db_properties import UserAttr, TableKey, TablePartition, HomeAttr
from internal import end
from item.helper.internal_helper import InternalHelper
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User


class Clear(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        home_id = valid_data[UserAttr.CURRENT_HOME]
        grid_slot = event[RequestField.Home.GRID]
        if not table.update_item(
            Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
            UpdateExpression=f"REMOVE #grid.#slot",
            ConditionExpression=f"attribute_exists(#id) and #slot in #grid",
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#grid": HomeAttr.GRID,
                "#slot": str(grid_slot),
            },
        ):
            end("Unable to clear grid slot data.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, str]:
        InternalHelper.validate_grid_request(
            target=event, message="Item Clear API (GRID SLOT)"
        )
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        if not user_data:
            end("Unable to retrieve current home for user.")
        return user_data
