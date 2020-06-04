from typing import no_type_check, Dict, Any

from database import table
from db_properties import TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, end
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User


class Go(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> Dict[str, Any]:
        home_index = event[RequestField.User.HOME] - 1
        home_id = valid_data[UserAttr.HOMES][home_index]
        response = table.get_item(
            Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
            ProjectionExpression="#grid, #meta",
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#grid": HomeAttr.GRID,
                "#meta": HomeAttr.META,
            },
        )
        if not (response and "Item" and response and response["Item"]):
            end("Unable to get home data for requested home.")
        if not User.update(user_id, UserAttr.CURRENT_HOME, home_id):
            end("Unable to set user current home to requested home.")
        return response["Item"]

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Any]:
        user_data = User.get(user_id, UserAttr.HOMES)
        if not user_data:
            end("Unable to retrieve homes list for user.")
        home_count = len(user_data[UserAttr.HOMES])
        validate_field(
            target=event,
            field=RequestField.User.HOME,
            validation=lambda value: type(value) is int and 0 < value <= home_count,
            message="Home select API",
        )
        return user_data
