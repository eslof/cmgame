from typing import Union
from collections.abc import Iterable
from botocore.exceptions import ClientError

from database import table
from internal import validate_field, end
from properties import TableKey, TablePartition, RequestField
from properties import UserState, UserAttr, Constants


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

        return event[RequestField.User.ID]

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
                end("Shouldn't be possible, attribute exists...")

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
            error = e.response["Error"]["Code"]
            if error == "ConditionalCheckFailedException":
                end("banned or nonexistant user?")
            end("Error: " + error)
        return True
