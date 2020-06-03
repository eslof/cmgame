from typing import Dict, Any

from botocore.exceptions import ClientError  # type: ignore

from database import table, db_get, db_update
from db_properties import TableKey, TablePartition, UserAttr
from internal import validate_field, end
from properties import RequestField, Constants


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
    def archive(user_id: str):
        return db_update(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
            UpdateExpression="set #partition = :user_archive",
            ConditionExpression=f"attribute_exists(#id)",
            ExpressionAttributeValues={":user_archive": TablePartition.USER_ARCHIVE},
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#partition": TableKey.PARTITION,
            },
        )

    @staticmethod
    def get(user_id: str, attributes: str) -> Dict[str, Any]:
        return db_get(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
            ProjectionExpression=attributes,
        )

    @staticmethod
    def update(
        user_id: str,
        attribute: str,
        value: Any,
        expression: str = "set #name = :value",
    ) -> bool:
        return db_update(
            Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
            UpdateExpression=expression,
            ConditionExpression=f"attribute_exists(#id)",
            ExpressionAttributeValues={":value": value,},
            ExpressionAttributeNames={"#name": attribute, "#id": TableKey.SORT,},
        )
