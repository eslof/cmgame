from request_handler import RequestHandler
from internal import validate_field, end
from properties import UserAttr, RequestField, Constants, TableKey, TablePartition
from user import User
from database import *


# TODO: research maybe using glacier to store deleted entries?
#   although it really doesn't matter since homes can be freely replicated at no expense
class Delete(RequestHandler):
    """Delete documentation"""

    @staticmethod
    def run(event: dict, user_data: dict, user_id: str) -> bool:
        """Run documentation TODO: stuff"""
        home_index = event[RequestField.User.HOME_INDEX]
        User.update(user_id, UserAttr.HOMES, home_index, "REMOVE #name[:value]")
        home_id = user_data[UserAttr.HOMES][home_index]
        try:
            table.delete_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id}
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            end(error)
            return False
        return True

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        """User.get HOMES """
        user_data = User.get(user_id, UserAttr.HOMES)
        validate_field(
            event,
            RequestField.User.HOME_INDEX,
            lambda value: isinstance(value, int)
            and 0 < value <= len(user_data[UserAttr.HOMES]),
            "Home delete API",
        )
        return user_data
