import json
from datetime import datetime
from typing import Dict, Any, Optional

from botocore.exceptions import ClientError  # type: ignore

from database import table, db_put, db_delete
from db_properties import TableKey, TablePartition, HomeAttr
from internal import generate_id, end


class HomeHelper:
    @staticmethod
    def template_new(home_id: str) -> Dict[str, Any]:
        time_now = datetime.now()
        time_string = time_now.strftime("%m-%d-%H-%M-%S")
        return {
            TableKey.PARTITION: TablePartition.HOME,
            TableKey.SORT: home_id,
            HomeAttr.META: json.dumps(dict(creation_date=time_string)),
            HomeAttr.GRID: {
                HomeAttr.MATCH_GRID_SLOT: {
                    HomeAttr.GridSlot.ITEM: HomeAttr.MATCH_GRID_SLOT,
                    HomeAttr.GridSlot.META: json.dumps({"color": "blue"}),
                }
            },
        }

    @classmethod
    def new(cls) -> Optional[str]:
        new_id = generate_id(HomeAttr.SORT_KEY_PREFIX)
        result = db_put(
            Item=cls.template_new(new_id),
            ConditionExpression="attribute_not_exists(#id)",
            ExpressionAttributeNames={"#id": TableKey.SORT},
        )
        return new_id if result else None

    @classmethod
    def delete(cls, home_id: str) -> bool:
        return db_delete(
            Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
            ConditionExpression="attribute_exists(#id)",
            ExpressionAttributeNames={"#id": TableKey.SORT},
        )
