from botocore.exceptions import ClientError
from typing import Optional

from database import table, TableKey, TablePartition, UserAttr
from internal import generate_id, end_unless_conditional
from properties import Constants, ResponseField, UserState, starting_inventory


class UserHelper:
    @staticmethod
    def welcome_attributes():
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
    def template_home(name: str, biodome: int):
        return {
            ResponseField.Home.NAME: name,
            ResponseField.Home.BIODOME: biodome,
        }

    @staticmethod
    def template_welcome(user_data: dict, homes: list, inventory: list):
        return {
            ResponseField.User.NAME: user_data[UserAttr.NAME],
            ResponseField.User.FLAG: user_data[UserAttr.FLAG],
            ResponseField.User.META: user_data[UserAttr.META],
            ResponseField.User.HOMES: homes,
            ResponseField.User.INVENTORY: inventory,
        }

    @staticmethod
    def template_new(new_id: str, name: str, flag: int) -> dict:
        """Database item template for a new User, assumes given parameters are valid."""
        return {
            TableKey.PARTITION: TablePartition.USER,
            TableKey.SORT: new_id,
            UserAttr.STATE: UserState.NEW.value,
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
    def attempt_new(cls, name: str, flag: int) -> Optional[str]:
        new_id = generate_id(UserAttr.SORT_KEY_PREFIX)
        try:
            # TODO: rework database model
            response = table.put_item(
                Item=cls.template_new(new_id=new_id, name=name, flag=flag),
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            end_unless_conditional(e)
            return None
        return new_id
