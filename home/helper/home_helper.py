from typing import Optional

from botocore.exceptions import ClientError

from internal import generate_id, end, end_unless_conditional
from properties import TableKey, HomeAttr, TablePartition, Constants
from database import *


class HomeHelper:
    @staticmethod
    def template_new(home_id: str):
        return {
            TableKey.PARTITION: TablePartition.HOME,
            TableKey.SORT: home_id,
            HomeAttr.META: "{}",
            HomeAttr.GRID: [{HomeAttr.Grid.ITEM: 0, HomeAttr.Grid.META: ""}]
            * Constants.Home.SIZE,
        }

    @classmethod
    def attempt_new(cls, batch_writer=None) -> Optional[str]:
        new_id = generate_id(HomeAttr.SORT_KEY_PREFIX)
        writer = batch_writer or table
        try:
            # TODO: rework database model template.
            writer.put_item(
                Item=cls.template_new(new_id),
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            end_unless_conditional(e)
            return None
        return new_id

    @classmethod
    def attempt_delete(cls, home_id: str, batch_writer=None):
        writer = batch_writer or table
        try:
            writer.delete_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                ConditionExpression="attribute_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.SORT},
            )
        except ClientError as e:
            end_unless_conditional(e)
            return False
        return True
