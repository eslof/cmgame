import json
from datetime import datetime
from typing import Dict, Any, Optional

from database import db_put, db_delete
from db_properties import TableKey, TablePartition, HomeAttr
from internal import generate_id
from properties import Constants


class HomeHelper:
    @staticmethod
    def _template_new(home_id: str) -> Dict[str, Any]:
        return {
            TableKey.PARTITION: TablePartition.HOME,
            TableKey.SORT: home_id,
            HomeAttr.META: json.dumps(
                {"creation_date": datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}
            ),
            HomeAttr.GRID: {
                HomeAttr.MATCH_GRID_SLOT: {
                    HomeAttr.GridSlot.ITEM: Constants.Home.MATCH_GRID_SLOT,
                    HomeAttr.GridSlot.META: json.dumps({"color": "blue"}),
                }
            },
        }

    @classmethod
    def new(cls) -> Optional[str]:
        new_id = generate_id(HomeAttr.SORT_KEY_PREFIX)
        return (
            new_id
            if db_put(
                Item=cls._template_new(new_id),
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.SORT},
            )
            else None
        )

    @classmethod
    def delete(cls, home_id: str) -> bool:
        return db_delete(
            Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
            ConditionExpression="attribute_exists(#id)",
            ExpressionAttributeNames={"#id": TableKey.SORT},
        )
