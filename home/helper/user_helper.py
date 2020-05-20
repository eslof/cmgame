from database import table, TableKey, TablePartition, UserAttr
from properties import UserState, Constants


class UserHelper:
    @staticmethod
    def template_home(home_id: str, name: str, biodome: int):
        return {
            UserAttr.Home.ID: home_id,
            UserAttr.Home.NAME: name,
            UserAttr.Home.BIODOME: biodome,
        }

    @classmethod
    def add_home(cls, user_id: str, home_id: str, name: str, biodome: int):
        table.update_item(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
            UpdateExpression=(
                "set #homes = list_append(#homes, :home), "
                "#home_count = #home_count + 1, "
            ),
            ConditionExpression=f"attribute_exists(#id) AND #state <> :banned AND #home_count <= :max_homes",
            ExpressionAttributeValues={
                ":banned": UserState.BANNED,
                ":max_homes": Constants.User.HOME_COUNT_MAX,
                ":home": cls.template_home(home_id, name, biodome),
            },
            ExpressionAttributeNames={
                "#id": TableKey.PARTITION,
                "#state": UserAttr.STATE,
                "#homes": UserAttr.HOMES,
                "#home_count": UserAttr.HOME_COUNT,
            },
        )
