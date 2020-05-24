from botocore.exceptions import ClientError  # type: ignore

from database import table, TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_field, validate_meta, end
from properties import Constants, RequestField
from request_handler import RequestHandler
from user_utils import User


class Place(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> bool:
        home_id = valid_data[UserAttr.CURRENT_HOME]
        item_slot = event[RequestField.User.ITEM]
        grid_slot = event[RequestField.Home.GRID]
        item_meta = event[RequestField.Item.META]
        try:
            table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"SET #grid.#grid_slot = :item",
                ConditionExpression=f"attribute_exists(#id)",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#grid": HomeAttr.GRID,
                    ":grid_slot": grid_slot,
                },
                ExpressionAttributeValues={
                    ":item": {
                        HomeAttr.GridSlot.ITEM: item_slot,
                        HomeAttr.GridSlot.META: item_meta,
                    },
                },
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])

        return True

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
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
