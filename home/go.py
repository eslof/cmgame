from typing import no_type_check, Dict, Any

from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, end
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User


class Go(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> dict:
        home_index = event[RequestField.User.HOME] - 1
        home_id = valid_data[UserAttr.HOMES][home_index]
        try:
            response = table.get_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                ProjectionExpression="#grid, #meta",
                ConditionExpression="attribute_exists(#id)",
                ExpressionAttributeNames={
                    "#id": TableKey.SORT,
                    "#grid": HomeAttr.GRID,
                    "#meta": HomeAttr.META,
                },
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])
        else:
            User.update(user_id, UserAttr.CURRENT_HOME, home_id)
            return response["Item"]

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Any]:
        user_data = User.get(user_id, UserAttr.HOMES)
        home_count = len(user_data[UserAttr.HOMES])
        validate_field(
            target=event,
            field=RequestField.User.HOME,
            validation=lambda value: type(value) is int and 0 < value <= home_count,
            message="Home select API",
        )
        return user_data
