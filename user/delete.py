from typing import no_type_check

from database import table, TablePartition, TableKey, UserAttr
from properties import UserState
from request_handler import RequestHandler


class Delete(RequestHandler):
    """TODO: CHANGE SORT KEY OF USER ITEM FROM USER TO USERARCHIVE"""

    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> None:
        # todo: error handling
        table.update_item(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
            UpdateExpression="set #partition = :user_archive",
            ConditionExpression=f"attribute_exists(#id) AND #state <> :banned",
            ExpressionAttributeValues={":user_archive": TablePartition.USER_ARCHIVE},
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#partition": TableKey.PARTITION,
            },
        )

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> None:
        return
