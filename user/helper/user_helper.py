from typing import Any, Dict, List, Union

from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr
from internal import generate_id, end_unless_conditional
from item_factory import DBItem
from properties import Constants, ResponseField, UserState, starting_inventory
from user.helper.item_helper import ItemHelper


class UserHelper:
    @staticmethod
    def welcome_info() -> Dict[str, List[DBItem]]:
        # TODO: no hard cody
        return {
            "biodomes": ItemHelper.get_biodomes(),
            "inventory": ItemHelper.get_starter_inventory(),
        }

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
        """Database item template for a new User, assumes given parameters are valid."""
        return {
            TableKey.PARTITION: TablePartition.USER,
            TableKey.SORT: new_id,
            UserAttr.STATE: UserState.NORMAL.value,
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
    def attempt_new(cls, name: str, flag: int) -> str:
        new_id = generate_id(UserAttr.SORT_KEY_PREFIX)
        try:
            # TODO: rework database model
            table.put_item(
                Item=cls.template_new(new_id=new_id, name=name, flag=flag),
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            end_unless_conditional(e)
            return ""
        return new_id
