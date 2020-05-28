from typing import Any, no_type_check, List, Union, Dict

from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr
from internal import validate_field, end
from properties import RequestField, UserState
from request_handler import RequestHandler
from user_utils import User
from itembox.helper.item_helper import ItemHelper


class Accept(RequestHandler):
    @classmethod
    @no_type_check
    def run(cls, event, user_id, valid_data) -> bool:
        seed = ItemHelper.itembox_seed(user_id, valid_data[UserAttr.KEY_USED_COUNT])
        item_id: int = ItemHelper.get_choice(
            valid_data[RequestField.ItemBox.CHOICE], seed, 3
        )
        try:
            if item_id in valid_data[UserAttr.INVENTORY]:
                cls._handle_duplicate(user_id)
            else:
                cls._handle_new(user_id, item_id)
        except ClientError as e:
            end(e.response["Error"]["Code"])
        return True

    @staticmethod
    def _handle_new(user_id: str, item_id: int) -> None:
        table.update_item(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id,},
            UpdateExpression=(
                "set #inventory = list_append(#inventory, :item_id), "
                "#key_count = #key_count - 1, "
                "#used_key_count = #used_key_count + 1"
            ),
            ConditionExpression=f"attribute_exists(#id) AND #state <> :banned",
            ExpressionAttributeValues={
                ":banned": UserState.BANNED.value,
                ":item_id": item_id,
            },
            ExpressionAttributeNames={
                "#id": TableKey.PARTITION,
                "#state": UserAttr.STATE,
                "#inventory": UserAttr.INVENTORY,
                "#key_count": UserAttr.KEY_COUNT,
                "#used_key_count": UserAttr.KEY_USED_COUNT,
            },
        )

    @staticmethod
    def _handle_duplicate(user_id: str) -> None:
        table.update_item(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id,},
            UpdateExpression="#used_key_count = #used_key_count + 1",
            ConditionExpression=f"attribute_exists(#id) AND #state <> :banned",
            ExpressionAttributeValues={":banned": UserState.BANNED.value,},
            ExpressionAttributeNames={
                "#id": TableKey.PARTITION,
                "#state": UserAttr.STATE,
                "#used_key_count": UserAttr.KEY_USED_COUNT,
            },
        )

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
