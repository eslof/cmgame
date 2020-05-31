from typing import Any, Dict

from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr
from home.helper.home_helper import HomeHelper
from internal import end
from properties import UserState, Constants


class UserHelper:
    # TODO: under construction
    @staticmethod
    def template_home(home_id: str, name: str, biodome: int) -> Dict[str, Any]:
        return {
            UserAttr.Home.ID: home_id,
            UserAttr.Home.NAME: name,
            UserAttr.Home.BIODOME: biodome,
        }

    @classmethod
    def add_home(cls, user_id: str, home_id: str, name: str, biodome: int) -> bool:
        try:
            table.update_item(
                Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
                UpdateExpression=(
                    "set #homes = list_append(#homes, :home), #home_count = #home_count + :one"
                ),
                ConditionExpression=f"attribute_exists(#id) AND #state <> :banned AND #home_count <= :max_homes",
                ExpressionAttributeNames={
                    "#id": TableKey.SORT,
                    "#state": UserAttr.STATE,
                    "#homes": UserAttr.HOMES,
                    "#home_count": UserAttr.HOME_COUNT,
                },
                ExpressionAttributeValues={
                    ":one": 1,
                    ":banned": UserState.BANNED.value,
                    ":max_homes": Constants.User.HOME_COUNT_MAX,
                    ":home": [cls.template_home(home_id, name, biodome)],
                },
            )
        except ClientError as e:
            HomeHelper.attempt_delete(home_id)
            error = e.response["Error"]["Code"]
            if error == "ConditionalCheckFailedException":
                end("No such user, banned user or home limit reached.")
            end(error)
        return True
