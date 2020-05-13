from properties import TableKey, TablePartition, HomeAttr, Constants, RequestField
from internal import validate_field, validate_meta, RequestHandler


class Update(RequestHandler):
    @staticmethod
    def run(home_id: str, grid_index: int, item_meta: str) -> bool:
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
        validate_field(
            target=event,
            field=RequestField.Home.GRID_INDEX,
            validation=lambda value: isinstance(value, int)
                                     and 0 < value <= Constants.Home.SIZE,
            validation_id="Item Update API (GRID_INDEX)",
        )
        validate_meta(
            target=event,
            field=RequestField.Item.META,
            validation_id="Item Update API (META)",
        )
