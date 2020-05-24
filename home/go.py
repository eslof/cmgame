from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, end
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User


class Go(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> dict:
        home_id = valid_data[UserAttr.HOMES][event[RequestField.User.HOME]]
        try:
            home_data = table.get_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                ProjectionExpression="#GRID, #META",
                ConditionExpression="attribute_exists(#id)",
                ExpressionAttributeNames={
                    "#ID": TableKey.SORT,
                    "#GRID": HomeAttr.GRID,
                    "#META": HomeAttr.META,
                },
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])
            return {}

        User.update(user_id, UserAttr.CURRENT_HOME, home_id)
        return home_data["Item"]

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        user_data = User.get(user_id, UserAttr.HOMES)
        home_count = len(user_data[UserAttr.HOMES])
        validate_field(
            target=event,
            field=RequestField.User.HOME,
            validation=lambda value: type(value) is int and 0 < value <= home_count,
            message="Home select API",
        )
        return user_data
