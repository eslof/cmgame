from properties import TableKey, TablePartition, HomeAttr, RequestField
from internal import sanitize_field, end


class Go:
    @staticmethod
    def run(home_id: str) -> list:
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

        # TODO: also update user current home

        return response["Item"][HomeAttr.ITEM_GRID]

    @staticmethod
    def sanitize(event: dict, home_count: int) -> None:
        sanitize_field(
            target=event,
            field=RequestField.User.HOME_INDEX,
            sanity=lambda value: isinstance(value, int) and 0 < value <= home_count,
            sanity_id="Home select API",
        )
