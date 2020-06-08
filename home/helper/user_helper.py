from typing import Any, Dict

from config import Config
from database import db_update
from db_properties import TableKey, TablePartition, UserAttr


class UserHelper:
    # TODO: under construction
    @staticmethod
    def _template_home(home_id: str, name: str, biodome: int) -> Dict[str, Any]:
        return {
            UserAttr.Home.ID: home_id,
            UserAttr.Home.NAME: name,
            UserAttr.Home.BIODOME: biodome,
        }

    @classmethod
    def add_home(cls, user_id: str, home_id: str, name: str, biodome: int) -> Any:
        return db_update(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
            UpdateExpression=(
                "set #homes = list_append(#homes, :home), #home_count = #home_count + :one"
            ),
            ConditionExpression=f"attribute_exists(#id) AND #home_count < :max_homes",
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#homes": UserAttr.HOMES,
                "#home_count": UserAttr.HOME_COUNT,
            },
            ExpressionAttributeValues={
                ":one": 1,
                ":max_homes": Config.HOME_COUNT_MAX,
                ":home": [cls._template_home(home_id, name, biodome)],
            },
        )
