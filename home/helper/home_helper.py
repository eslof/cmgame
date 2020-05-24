import json
from datetime import datetime
from typing import Optional

from botocore.exceptions import ClientError  # type: ignore

from database import table, TableKey, TablePartition, HomeAttr
from internal import generate_id, end_unless_conditional, end


class HomeHelper:
    @staticmethod
    def template_new(home_id: str):
        # TODO: update! it would cost too much wcu to do this
        #  grid has to be dict populated over time not list
        time_now = datetime.now()
        time_string = time_now.strftime("%m-%d-%H-%M-%S")
        return {
            TableKey.PARTITION: TablePartition.HOME,
            TableKey.SORT: home_id,
            HomeAttr.META: json.dumps(dict(creation_date=time_string)),
            HomeAttr.GRID: {
                HomeAttr.MATCH_GRID_SLOT: {
                    HomeAttr.GridSlot.ITEM: HomeAttr.MATCH_GRID_SLOT,
                    HomeAttr.GridSlot.META: json.dumps(dict(color="blue")),
                }
            },
        }

    @classmethod
    def attempt_new(cls) -> str:
        new_id = generate_id(HomeAttr.SORT_KEY_PREFIX)
        try:
            # TODO: rework database model template.
            table.put_item(
                Item=cls.template_new(new_id),
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])
            return ""
        return new_id

    @classmethod
    def attempt_delete(cls, home_id: str):
        try:
            table.delete_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                ConditionExpression="attribute_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.SORT},
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])
        return True
