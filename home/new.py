from base64 import b64encode
from encrypt import password_encrypt

from request_handler import RequestHandler
from properties import RequestField, TableKey, HomeAttr, UserAttr, TablePartition
from properties import Secret, Constants, Biodome
from internal import validate_field, generate_id, end
from database import *
from user import User


class New(RequestHandler):
    """User requests to create a new home."""

    @staticmethod
    def run(event: dict, user_id: str, data: dict, recursion_limit: int = 3) -> bool:
        """TODO: this entire thing needs a rework: there need be a template for user item
        TODO: should it be recursive or is there a better way?"""
        home_id = generate_id()
        home = {
            TableKey.PARTITION: TablePartition.HOME,
            TableKey.SORT: home_id,
            HomeAttr.META: "",
            HomeAttr.GRID: [{HomeAttr.Grid.ITEM: 0, HomeAttr.Grid.META: ""}]
            * Constants.Home.SIZE,
        }
        try:
            # TODO: rework database model template.
            response = table.put_item(
                Item=home,
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]  # TODO: error handling
            if error == "ConditionalCheckFailedException" and recursion_limit > 0:
                recursion_limit -= 1
                return New.run(event, user_data, user_id, recursion_limit)
            return False
        User.add_home(user_id, home_id)
        return True

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        """Confirm name to be of appropriate length, and existence of requested Biodome."""
        user_data = User.get(user_id, UserAttr.HOMES)
        home_count = len(user_data[UserAttr.HOMES])
        if home_count > Constants.User.HOME_COUNT_MAX:
            end("Maximum homes reached")  # TODO: error handling
        validate_field(
            target=event,
            field=RequestField.Home.NAME,
            validation=lambda value: isinstance(value, str)
            and 0 < len(value) <= Constants.Home.NAME_MAX_LENGTH,
            message="Home Create API (NAME)",
        )
        validate_field(
            target=event,
            field=RequestField.Home.BIODOME,
            validation=lambda value: isinstance(value, int)
            and value in Biodome._value2member_map_,
            message="Home Create API (BIODOME)",
        )
        return user_data
