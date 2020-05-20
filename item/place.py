from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, validate_meta
from properties import Constants, RequestField
from request_handler import RequestHandler
from user import User


class Place(RequestHandler):
    """User requests to change the contents of a grid slot in the user's selected home."""

    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> bool:
        """Sets a grid slot for given home id to contain a requested item with given meta data."""
        home_id = valid_data[UserAttr.CURRENT_HOME]
        item_index = event[RequestField.User.ITEM] - 1
        grid_index = event[RequestField.Home.GRID] - 1
        item_meta = event[RequestField.Item.META]
        try:
            # TODO: rework database model
            response = table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"SET #grid[#index].#item = :item, #grid[#index].#meta = :meta",
                ConditionExpression=f"attribute_exists(#id)",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#grid": HomeAttr.GRID,
                    "#item": HomeAttr.Grid.ITEM,
                    "#meta": HomeAttr.Grid.META,
                    "#index": grid_index,
                },
                ExpressionAttributeValues={":index": item_index, ":meta": item_meta,},
            )
        except ClientError as e:
            # TODO: error handling
            return False
            # if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            #    return False
            # end("Missing home? " + e.response["Error"]["Code"])

        return True

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        """Confirm item index to be in range of inventory size.
        Confirm target grid index to be in range of home size.
        Confirm that item meta-data follows correct format and TODO: apply size limitation in case of misuse."""
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.INVENTORY_COUNT}, {UserAttr.CURRENT_HOME}",
        )
        inventory_count = user_data[UserAttr.INVENTORY_COUNT]
        validate_field(
            target=event,
            field=RequestField.User.ITEM,
            validation=lambda value: type(value) is int
            and 0 < value <= inventory_count,
            message="Item Place API (ITEM_INDEX)",
        )
        validate_field(
            target=event,
            field=RequestField.Home.GRID,
            validation=lambda value: type(value) is int
            and 0 < value <= Constants.Home.SIZE,
            message="Item Place API (GRID)",
        )
        validate_meta(
            target=event, field=RequestField.Item.META, message="Item Place API (META)",
        )
        return user_data
