from database import TableKey, UserAttr, TablePartition, table
from properties import UserState


class UserHelper:
    @staticmethod
    def handle_new_item(user_id: str, item_id: int) -> None:
        # TODO: error handling
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
                "#id": TableKey.SORT,
                "#state": UserAttr.STATE,
                "#inventory": UserAttr.INVENTORY,
                "#key_count": UserAttr.KEY_COUNT,
                "#used_key_count": UserAttr.KEY_USED_COUNT,
            },
        )

    @staticmethod
    def handle_duplicate_item(user_id: str) -> None:
        table.update_item(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id,},
            UpdateExpression="#used_key_count = #used_key_count + 1",
            ConditionExpression=f"attribute_exists(#id) AND #state <> :banned",
            ExpressionAttributeValues={":banned": UserState.BANNED.value},
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#state": UserAttr.STATE,
                "#used_key_count": UserAttr.KEY_USED_COUNT,
            },
        )
