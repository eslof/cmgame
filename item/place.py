from typing import no_type_check, Union, Dict

from botocore.exceptions import ClientError  # type: ignore

from database import table, db_update
from db_properties import TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, validate_meta, end
from item.helper.internal_helper import InternalHelper
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User


class Place(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        if not db_update(
            Key={
                TableKey.PARTITION: TablePartition.HOME,
                TableKey.SORT: valid_data[UserAttr.CURRENT_HOME],
            },
            UpdateExpression=f"SET #grid.#grid_slot = :item",
            ConditionExpression=f"attribute_exists(#id)",
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#grid": HomeAttr.GRID,
                "#grid_slot": event[RequestField.Home.GRID],
            },
            ExpressionAttributeValues={
                ":item": {
                    HomeAttr.GridSlot.ITEM: event[RequestField.User.ITEM],
                    HomeAttr.GridSlot.META: event[RequestField.Item.META],
                },
            },
        ):
            end("Unable to update selected grid slot.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Union[int, str]]:
        InternalHelper.validate_grid_request(
            target=event, message="Item Place API (GRID SLOT)"
        )
        validate_meta(
            target=event, field=RequestField.Item.META, message="Item Place API (META)",
        )
        user_data = User.get(
            user_id, f"{UserAttr.INVENTORY_COUNT}, {UserAttr.CURRENT_HOME}",
        )
        if not user_data:
            end("Unable to retrieve inventory and current home for user.")
        validate_field(
            target=event,
            field=RequestField.User.ITEM,
            validation=lambda value: type(value) is int
            and 0 < value <= user_data[UserAttr.INVENTORY_COUNT],
            message="Item Place API (ITEM REFERENCE)",
        )
        return user_data
