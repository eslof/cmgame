from typing import Any

from .helper.item_helper import ItemHelper
from database import table, TableKey, TablePartition, UserAttr
from internal import validate_field, end
from properties import RequestField, UserState
from request_handler import RequestHandler
from user import User


class Accept(RequestHandler):
    """User responds to a demanded itembox with requested choice."""

    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> Any:
        inventory = valid_data[UserAttr.INVENTORY]
        seed = ItemHelper.itembox_seed(
            user_id, valid_data[UserAttr.KEY_COUNT], valid_data[UserAttr.KEY_USED_COUNT]
        )
        choices = ItemHelper.itembox(3, seed, inventory)
        table.update_item(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
            UpdateExpression=(
                "set #inventory = list_append(#inventory, :item_id), "
                "#key_count = #key_count - 1, "
                "#used_key_count = #used_key_count + 1"
            ),
            ConditionExpression=f"attribute_exists(#id) AND #state <> :banned",
            ExpressionAttributeValues={
                ":banned": UserState.BANNED,
                ":item_id": choices[event[RequestField.ItemBox.CHOICE]],
            },
            ExpressionAttributeNames={
                "#id": TableKey.PARTITION,
                "#state": UserAttr.STATE,
                "#inventory": UserAttr.INVENTORY,
                "#key_count": UserAttr.KEY_COUNT,
                "#used_key_count": UserAttr.KEY_USED_COUNT,
            },
        )
        return choices[event[RequestField.ItemBox.CHOICE] - 1]
        pass

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
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
