from properties import TableKey, TablePartition, HomeAttr, RequestField, UserAttr
from internal import validate_field, end, RequestHandler
from user import User


class Go(RequestHandler):
    """User requests to be moved to one of the user's own homes."""

    @staticmethod
    def run(user_id: str, home_id: str) -> list:
        """Set selected home of given user id to given home id.
         Get and return grid and associated meta-data for given home id."""

        try:
            # TODO: rework database model also dont forget to get home meta data
            response = table.get_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                ProjectionExpression="#GRID, #META, #ITEM_META",
                ExpressionAttributeNames={
                    "#GRID": HomeAttr.GRID,
                    "#META": HomeAttr.META,
                    "#ITEM_META": HomeAttr.ITEM_META,
                },
            )
        except ClientError as e:
            end(e.response["Error"]["Message"])  # TODO: error-handling
            # this avoids complains about unassigned reference to response return var
            return []
        else:
            if "Item" not in response or len(response["Item"]) < 1:
                # TODO: figure this out
                end("No such user found")

        # TODO: also update user current home
        response = User.update(UserAttr.CURRENT_HOME, home_id)

        return response["Item"][HomeAttr.GRID]

    @staticmethod
    def validate(event: dict, home_count: int) -> None:
        """Confirm requested index to be in range of user's home count."""

        validate_field(
            target=event,
            field=RequestField.User.HOME_INDEX,
            validation=lambda value: isinstance(value, int) and 0 < value <= home_count,
            message="Home select API",
        )
