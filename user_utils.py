from collections.abc import Iterable
from typing import Union, Dict, Any

from botocore.exceptions import ClientError  # type: ignore

from database import table, TableKey, TablePartition, UserAttr
from internal import validate_field, end
from properties import RequestField, UserState, Constants


class User:
    @staticmethod
    def validate_id(event: Dict[str, str]) -> str:
        # TODO: real user authentication
        validate_field(
            target=event,
            field=RequestField.User.ID,
            validation=lambda value: type(value) is str
            and len(value) == Constants.EXPECTED_ID_LEN,
            message="User authentication API",
        )

        return event[RequestField.User.ID]

    @staticmethod
    def get(user_id: str, attributes: str) -> Dict[str, Any]:
        """Get and return given attributes for given user_id unless banned."""
        try:
            response: Dict[str, Dict[str, Any]] = table.get_item(
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
            end(e.response["Error"]["Code"])
            return {}
        else:
            return response["Item"]

    @staticmethod
    def update(
        user_id: str,
        attribute: str,
        value: Any,
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
            end(e.response["Error"]["Code"])
        return True
