from typing import Dict, Any, Optional

from database import db_get, db_update
from db_properties import TableKey, TablePartition
from internal import validate_field
from properties import RequestField, Constants


class UserUtils:
    @staticmethod
    def validate_id(event: Dict[str, str]) -> str:
        validate_field(
            target=event,
            field=RequestField.User.ID,
            value_type=str,
            validation=lambda v: len(v) == Constants.EXPECTED_ID_LEN,
            message="User authentication API",
        )

        return event[RequestField.User.ID]  # pop it? or leave it and let by event?

    @staticmethod
    def get(user_id: str, attributes: str) -> Optional[Dict[str, Any]]:
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
            ExpressionAttributeValues={":value": value},
            ExpressionAttributeNames={"#name": attribute, "#id": TableKey.SORT},
        )
