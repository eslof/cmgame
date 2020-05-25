from typing import no_type_check, Dict

from botocore.exceptions import ClientError  # type: ignore

from database import UserAttr, TableKey, TablePartition, HomeAttr, table
from internal import end, validate_field
from properties import RequestField, Constants
from request_handler import RequestHandler
from user_utils import User


class Clear(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        home_id = valid_data[UserAttr.CURRENT_HOME]
        grid_slot = event[RequestField.Home.GRID]
        try:
            table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"REMOVE #grid.#slot",
                ConditionExpression=f"attribute_exists(#id) and #slot in #grid",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#grid": HomeAttr.GRID,
                    "#slot": grid_slot,
                },
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, str]:
        validate_field(
            target=event,
            field=RequestField.Home.GRID,
            validation=lambda value: type(value) is int
            and 0 < value <= Constants.Home.SIZE,
            message="Item Place API (ITEM_INDEX)",
        )
        return User.get(user_id, UserAttr.CURRENT_HOME)
