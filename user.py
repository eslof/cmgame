from typing import Union
from collections.abc import Iterable

from database import *
from internal import validate_field, end, generate_id
from properties import TableKey, TablePartition, RequestField
from properties import Seed, Constants, starting_inventory
from properties import UserState, QueueState, UserAttr
from encrypt import password_decrypt


class User:
    @staticmethod
    def validate_id(event: dict) -> str:
        """TODO: user authentication"""
        validate_field(
            target=event,
            field=RequestField.User.ID,
            validation=lambda value: isinstance(value, str)
            and len(value) == Constants.ID_CHAR_LENGTH,
            message="User authentication API",
        )

        return password_decrypt(
            token=event[RequestField.User.ID], password=Seed.USER_ID
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
    def update(
        user_id: str,
        attribute: str,
        value: Union[int, str, bool, Iterable],
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
