from typing import Optional

from internal import generate_id, end
from properties import (
    TablePartition,
    TableKey,
    UserAttr,
    UserState,
    ResponseField,
    ItemAttr,
)
from properties import QueueState, Constants, starting_inventory
from database import *


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
            UserAttr.CURRENT_HOME: "",
            UserAttr.QUEUE_STATE: QueueState.NONE.value,
            UserAttr.LIST_ID: "",
            UserAttr.KEY_COUNT: Constants.User.STARTING_KEY_COUNT,
            UserAttr.USED_KEY_COUNT: 0,
            UserAttr.INVENTORY: starting_inventory,
            UserAttr.INVENTORY_COUNT: len(starting_inventory),
            UserAttr.HOMES: [],
        }

    @classmethod
    def attempt_new(cls, name, flag) -> Optional[str]:
        new_id = generate_id(UserAttr.SORT_KEY_PREFIX)
        try:
            # TODO: rework database model
            response = table.put_item(
                Item=cls.template_new(new_id=new_id, name=name, flag=flag),
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            if error != "ConditionalCheckFailedException":
                end("Error: " + error)  # TODO: error handling
            return None
        return new_id
