from typing import Union

from database import *
from internal import validate_field, end, generate_id
from item import Item
from properties import (
    RequestField,
    TableKey,
    TablePartition,
    Secret,
    starting_inventory,
)
from properties import Constants, UserState, QueueState, UserAttr
from encrypt import password_decrypt

"""
    STATE = "state"
    NAME = "name"
    FLAG = "flag"
    META = "meta"
    CURRENT_HOME = "current_home"
    QUEUE_STATE = "queue_state"
    LIST_ID = "match"
    KEY_COUNT = "keys"
    USED_KEY_COUNT = "used_keys"
    INVENTORY_COUNT = "inventory_count"
    INVENTORY = "inventory"
    HOMES = "homes"
    """


class User:
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

    @staticmethod
    def validate_id(event: dict) -> str:
        """TODO: user authentication"""
        validate_field(
            target=event,
            field=RequestField.User.ID,
            validation=lambda value: isinstance(value, str)
            and len(value) == Constants.User.EXPECTED_ID_LENGTH,
            message="User authentication API",
        )

        return password_decrypt(
            token=event[RequestField.User.ID], password=Secret.USER_ID
        )

    @staticmethod
    def get(user_id: str, attributes: str) -> dict:
        """Get and return given attributes for given user_id unless banned."""
        try:
            # TODO: rework db
            response = table.get_item(
                Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
                ProjectionExpression=attributes,
                ConditionExpression=f"attribute_exists(#id) AND #state <> :banned",
                ExpressionAttributeValues={":banned": UserState.BANNED.value},
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#state": UserAttr.STATE,
                },
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            if error == "ConditionalCheckFailedException":
                end("banned or nonexistent user?")
            end("Error: " + error)  # TODO: fix some of this error handling
        else:
            if len(response["Item"]) == 0:
                end("Unable to find user for given UUID.")

            return response["Item"]

    @staticmethod
    def add_home(user_id: str, home_id: str):
        return User.update(
            user_id, UserAttr.HOMES, home_id, "set #homes = list_append(#homes, :value)"
        )

    @staticmethod
    def update(
        user_id: str,
        attribute: str,
        value: Union[int, str, bool, set],
        expression: str = "set #name = :value",
    ) -> bool:
        try:
            table.update_item(
                Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
                UpdateExpression=expression,
                ConditionExpression=f"attribute_exists(#id) AND #state <> :banned",
                ExpressionAttributeValues={
                    ":value": value,
                    ":banned": UserState.BANNED.value,
                },
                ExpressionAttributeNames={
                    "#name": attribute,
                    "#id": TableKey.PARTITION,
                    "#state": UserAttr.STATE,
                },
            )
        except ClientError as e:
            # error = e.response["Error"]["Code"]
            # if error == "ConditionalCheckFailedException":
            #    end("banned or nonexistant user?")
            # end("Error: " + error)  # TODO: fix some of this error handling
            return False

        return True

    @staticmethod
    def attempt_new(name, flag) -> str:
        new_id = generate_id()
        try:
            # TODO: rework database model
            response = table.put_item(
                Item=User.template_new(new_id=new_id, name=name, flag=flag),
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            if error != "ConditionalCheckFailedException":
                end("Error: " + error)  # TODO: error handling
            return ""
        return new_id
