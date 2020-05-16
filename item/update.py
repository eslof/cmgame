from request_handler import RequestHandler
from properties import TableKey, TablePartition, HomeAttr, Constants, RequestField
from internal import validate_field, validate_meta
from database import *


class Update(RequestHandler):
    """User requests to update the meta-data of an item in the user's selected home."""

    @staticmethod
    def run(home_id: str, grid_index: int, item_meta: str) -> bool:
        """Sets given item meta-data at requested grid index for the given home id"""
        try:
            # TODO: rework database model
            response = table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"SET #meta.#grid_index = :item_meta",
                ConditionExpression=f"attribute_exists(#id)",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#meta": HomeAttr.META,
                    "#grid_index": grid_index,
                },
                ExpressionAttributeValues={":item_meta": item_meta},
            )
        except ClientError as e:
            # TODO: error handling
            return False
            # error = e.response['Error']['Code']
            # if error != 'ConditionalCheckFailedException':
            #     end("Error: " + error)
            # end("Item already selected (or missing home): " + error)

        return True

    @staticmethod
    def validate(event: dict) -> None:
        """Confirm target grid index to be in range of home size.
        Confirm that item meta-data follows correct format and TODO: apply size limitation in case of misuse."""
        validate_field(
            target=event,
            field=RequestField.Home.GRID_INDEX,
            validation=lambda value: isinstance(value, int)
            and 0 < value <= Constants.Home.SIZE,
            message="Item Update API (GRID_INDEX)",
        )
        validate_meta(
            target=event,
            field=RequestField.Item.META,
            message="Item Update API (META)",
        )
