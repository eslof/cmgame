from properties import TableKey, TablePartition, HomeAttr, RequestField
from internal import validate_field, end, RequestHandler


class Go(RequestHandler):
    """User requests to be moved to one of the user's own homes."""

    @staticmethod
    def run(home_id: str) -> list:
        """Home grid is fetched along with associated meta-data for given home id and pushed to View."""

        try:
            # TODO: rework database model also dont forget to get home meta data
            response = table.get_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                ProjectionExpression="#GRID",
                ExpressionAttributeNames={"#GRID": HomeAttr.ITEM_GRID},
            )
        except ClientError as e:
            end(e.response["Error"]["Message"])  # TODO: error-handling
            # this avoids complains about unassigned reference to response return var
            return []
        else:
            if "Item" not in response:
                # TODO: figure this out
                end("No such user found")
        # TODO: meta data
        # TODO: also update user current home
        # TODO: biodome is delivered at welcome and could be delivered at match found but we might as well always send
        return response["Item"][HomeAttr.ITEM_GRID]

    @staticmethod
    def validate(event: dict, home_count: int) -> None:
        """Confirm requested home index to fall in the range of user's home count."""

        validate_field(
            target=event,
            field=RequestField.User.HOME_INDEX,
            validation=lambda value: isinstance(value, int) and 0 < value <= home_count,
            message="Home select API",
        )
