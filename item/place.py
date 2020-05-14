from properties import TableKey, TablePartition, HomeAttr, RequestField, Constants
from internal import validate_field, validate_meta, RequestHandler


class Place(RequestHandler):
    """User requests to change the contents of a grid slot in the user's selected home."""

    @staticmethod
    def run(home_id: str, item_index: int, grid_index: int, item_meta: str) -> bool:
        """Sets a grid slot for home id to contain a requested item with meta data."""
        try:
            # TODO: rework database model
            response = table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"SET #item_grid.#grid_index = :item_index, #item_meta.#grid_index = :item_meta",
                ConditionExpression=f"attribute_exists(#id)",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#item_grid": HomeAttr.ITEM_GRID,
                    "#item_meta": HomeAttr.ITEM_META,
                    "#grid_index": grid_index,
                    "#item_index": item_index,
                },
                ExpressionAttributeValues={
                    ":item_index": item_index,
                    ":item_meta": item_meta,
                },
            )
        except ClientError as e:
            # TODO: error handling
            return False
            # if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
            #    return False
            # end("Missing home? " + e.response["Error"]["Code"])

        return True

    @staticmethod
    def validate(event: dict, inventory_size: int) -> None:
        """Confirm item index to be in range of inventory size.
        Confirm target grid index to be in range of home size.
        Confirm that item meta-data follows correct format and TODO: apply size limitation in case of misuse."""
        validate_field(
            target=event,
            field=RequestField.User.ITEM_INDEX,
            validation=lambda value: isinstance(value, int)
            and 0 < value <= inventory_size,
            message="Item Place API (ITEM_INDEX)",
        )
        validate_field(
            target=event,
            field=RequestField.Home.GRID_INDEX,
            validation=lambda value: isinstance(value, int)
            and 0 < value <= Constants.Home.SIZE,
            message="Item Place API (GRID_INDEX)",
        )
        validate_meta(
            target=event, field=RequestField.Item.META, message="Item Place API (META)",
        )
