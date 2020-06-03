from typing import Any, Dict, List, Union, Optional

from botocore.exceptions import ClientError

from database import table, db_put
from db_properties import TableKey, TablePartition, UserAttr
from internal import generate_id, end_unless_conditional, end
from properties import Constants, ResponseField, starting_inventory


class UserHelper:
    @staticmethod
    def welcome_attributes() -> str:
        return ", ".join(
            [
                UserAttr.NAME,
                UserAttr.FLAG,
                UserAttr.META,
                UserAttr.HOMES,
                UserAttr.INVENTORY,
            ]
        )

    @staticmethod
    def template_home(name: str, biodome: int) -> Dict[str, Any]:
        return {
            ResponseField.Home.NAME: name,
            ResponseField.Home.BIODOME: biodome,
        }

    @staticmethod
    def template_welcome(
        user_data: Dict[str, Any],
        homes: List[Dict[str, Union[str, int]]],
        inventory: List[Dict[str, Union[str, int]]],
    ) -> Dict[str, Any]:
        return {
            ResponseField.User.NAME: user_data[UserAttr.NAME],
            ResponseField.User.FLAG: user_data[UserAttr.FLAG],
            ResponseField.User.META: user_data[UserAttr.META],
            ResponseField.User.HOMES: homes,
            ResponseField.User.INVENTORY: inventory,
        }

    @staticmethod
    def template_new(new_id: str, name: str, flag: int) -> Dict[str, Any]:
        return {
            TableKey.PARTITION: TablePartition.USER,
            TableKey.SORT: new_id,
            UserAttr.NAME: name,
            UserAttr.FLAG: flag,
            UserAttr.META: "{}",
            UserAttr.MATCH_ID: "",
            UserAttr.CURRENT_HOME: "",
            UserAttr.HOMES: [],
            UserAttr.HOME_COUNT: 0,
            UserAttr.KEY_COUNT: Constants.User.STARTING_KEY_COUNT,
            UserAttr.KEY_USED_COUNT: 0,
            UserAttr.INVENTORY: starting_inventory,
            UserAttr.INVENTORY_COUNT: len(starting_inventory),
        }

    @classmethod
    def new(cls, name: str, flag: int) -> Optional[str]:
        new_id = generate_id(UserAttr.SORT_KEY_PREFIX)
        results = db_put(
            Item=cls.template_new(new_id=new_id, name=name, flag=flag),
            ConditionExpression="attribute_not_exists(#id)",
            ExpressionAttributeNames={"#id": TableKey.SORT},
        )
        if not results:
            return None
        return new_id
