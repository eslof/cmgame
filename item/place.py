from properties import TableKey, TablePartition, HomeAttr, RequestField, Constants
from internal import sanitize_field, sanitize_json, RequestHandler


class Place(RequestHandler):
    @staticmethod
    def run(home_id: str, item_index: int, grid_index: int, item_meta: str) -> bool:
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
    def sanitize(event: dict, inventory_size: int) -> None:
        sanitize_field(
            target=event,
            field=RequestField.User.ITEM_INDEX,
            sanity=lambda value: isinstance(value, int) and 0 < value <= inventory_size,
            sanity_id="Item Place API (ITEM_INDEX)",
        )
        sanitize_field(
            target=event,
            field=RequestField.Home.GRID_INDEX,
            sanity=lambda value: isinstance(value, int)
            and 0 < value <= Constants.Home.SIZE,
            sanity_id="Item Place API (GRID_INDEX)",
        )
        sanitize_json(
            target=event,
            field=RequestField.Item.META,
            sanity_id="Item Place API (META)",
        )
