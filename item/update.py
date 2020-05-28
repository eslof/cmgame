from typing import Dict, no_type_check

from botocore.exceptions import ClientError  # type: ignore

from database import table, TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, validate_meta, end
from item.helper.internal_helper import InternalHelper
from properties import Constants, RequestField
from request_handler import RequestHandler
from user_utils import User


class Update(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        home_id = valid_data[UserAttr.CURRENT_HOME]
        grid_slot = event[RequestField.Home.GRID]
        item_meta = event[RequestField.Item.META]
        try:
            # TODO: rework database model
            table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"SET #grid.#grid_slot.#slot_meta = :item_meta",
                ConditionExpression=f"attribute_exists(#id) and #grid_slot in #grid",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#grid": HomeAttr.GRID,
                    "#slot_meta": HomeAttr.GridSlot.META,
                    "#grid_slot": grid_slot,
                },
                ExpressionAttributeValues={":item_meta": item_meta},
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, str]:
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        InternalHelper.validate_grid_request(
            target=event, message="Item Update API (GRID SLOT)"
        )
        validate_meta(
            target=event,
            field=RequestField.Item.META,
            message="Item Update API (META)",
        )
        return user_data
