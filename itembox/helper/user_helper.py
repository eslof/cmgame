from database import db_update
from db_properties import TableKey, UserAttr, TablePartition


class UserHelper:
    @staticmethod
    def handle_new_item(user_id: str, item_id: int) -> bool:
        return db_update(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id,},
            UpdateExpression=(
                "set #inventory = list_append(#inventory, :item_id), "
                "#key_count = #key_count - 1, "
                "#used_key_count = #used_key_count + 1"
            ),
            ConditionExpression=f"attribute_exists(#id)",
            ExpressionAttributeValues={":item_id": item_id,},
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#inventory": UserAttr.INVENTORY,
                "#key_count": UserAttr.KEY_COUNT,
                "#used_key_count": UserAttr.KEY_USED_COUNT,
            },
        )

    @staticmethod
    def handle_duplicate_item(user_id: str) -> bool:
        return db_update(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id,},
            UpdateExpression="#used_key_count = #used_key_count + 1",
            ConditionExpression=f"attribute_exists(#id)",
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#used_key_count": UserAttr.KEY_USED_COUNT,
            },
        )
