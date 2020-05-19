from database import table, TableKey, TablePartition, UserAttr
from internal import validate_field, validate_meta
from properties import Constants, RequestField
from request_handler import RequestHandler
from user import User


class Update(RequestHandler):
    """User requests to update the meta-data of an item in the user's selected home."""

    @staticmethod
    def run(body: dict, user_id: str, data: dict) -> bool:
        """Sets given item meta-data at requested grid index for the given home id"""
        home_id = (data[UserAttr.CURRENT_HOME],)
        grid_index = (body[RequestField.Home.GRID],)
        item_meta = body[RequestField.Item.META]
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
    def validate(body: dict, user_id: str) -> dict:
        """Confirm target grid index to be in range of home size.
        Confirm that item meta-data follows correct format and TODO: apply size limitation in case of misuse."""
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        validate_field(
            target=body,
            field=RequestField.Home.GRID,
            validation=lambda value: isinstance(value, int)
            and 0 < value <= Constants.Home.SIZE,
            message="Item Update API (GRID)",
        )
        validate_meta(
            target=body, field=RequestField.Item.META, message="Item Update API (META)",
        )
        return user_data
