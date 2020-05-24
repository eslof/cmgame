from botocore.exceptions import ClientError  # type: ignore

from database import table, TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, validate_meta, end
from properties import Constants, RequestField
from request_handler import RequestHandler
from user_utils import User


class Update(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> bool:
        home_id = valid_data[UserAttr.CURRENT_HOME]
        grid_slot = event[RequestField.Home.GRID]
        item_meta = event[RequestField.Item.META]
        try:
            # TODO: rework database model
            table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"SET #grid.#grid_slot.#slot_meta = :item_meta",
                ConditionExpression=f"attribute_exists(#id) and :grid_slot in #grid",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#grid": HomeAttr.GRID,
                    "#slot_meta": HomeAttr.GridSlot.META,
                    "#grid_slot": grid_slot,
                },
                ExpressionAttributeValues={":item_meta": item_meta},
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])

        return True

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        validate_field(
            target=event,
            field=RequestField.Home.GRID,
            validation=lambda value: type(value) is int
            and 0 < value <= Constants.Home.SIZE,
            message="Item Update API (GRID)",
        )
        validate_meta(
            target=event,
            field=RequestField.Item.META,
            message="Item Update API (META)",
        )
        return user_data
