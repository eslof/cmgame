from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, end
from properties import RequestField
from request_handler import RequestHandler
from user import User


class Go(RequestHandler):
    """User requests to be moved to one of the user's own homes."""

    @staticmethod
    def run(event: dict, user_id: str, data: dict) -> dict:
        """Set selected home of given user id to given home id.
         Get and return grid and associated meta-data for given home id."""
        home_id = data[UserAttr.HOMES][event[RequestField.User.HOME]]
        try:
            # TODO: rework database model also dont forget to get home meta data
            home_data = table.get_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                ProjectionExpression="#GRID, #META",
                ExpressionAttributeNames={
                    "#GRID": HomeAttr.GRID,
                    "#META": HomeAttr.META,
                },
            )
        except ClientError as e:
            end(e.response["Error"]["Message"])  # TODO: error-handling
            # this avoids complains about unassigned reference to response return var
            return {}
        else:
            if "Item" not in home_data or len(home_data["Item"]) < 1:
                # TODO: figure this out
                end("No such user found")

        User.update(user_id, UserAttr.CURRENT_HOME, home_id)

        return home_data["Item"]

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        """Confirm requested index to be in range of user's home count."""
        # TODO: possibly batch write update_item to set current home with a condition?
        user_data = User.get(user_id, UserAttr.HOMES)
        home_count = len(user_data[UserAttr.HOMES])
        validate_field(
            target=event,
            field=RequestField.User.HOME,
            validation=lambda value: isinstance(value, int) and 0 < value <= home_count,
            message="Home select API",
        )
        return user_data
