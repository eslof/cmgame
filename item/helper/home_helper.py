from database import db_update
from db_properties import TableKey, HomeAttr, TablePartition


class HomeHelper:
    @staticmethod
    def clear_slot(home_id, grid_slot):
        return db_update(
            Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
            UpdateExpression=f"REMOVE #grid.#slot",
            ConditionExpression=f"attribute_exists(#id) and #slot in #grid",
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#grid": HomeAttr.GRID,
                "#slot": str(grid_slot),
            },
        )

    @staticmethod
    def set_slot(home_id, grid_slot, item, meta):
        return db_update(
            Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id,},
            UpdateExpression=f"SET #grid.#grid_slot = :item",
            ConditionExpression=f"attribute_exists(#id)",
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#grid": HomeAttr.GRID,
                "#grid_slot": grid_slot,
            },
            ExpressionAttributeValues={
                ":item": {HomeAttr.GridSlot.ITEM: item, HomeAttr.GridSlot.META: meta,},
            },
        )

    @staticmethod
    def update(home_id, grid_slot, item_meta):
        return db_update(
            Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
            UpdateExpression=f"SET #grid.#grid_slot.#slot_meta = :item_meta",
            ConditionExpression=f"attribute_exists(#id) and #grid_slot in #grid",
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#grid": HomeAttr.GRID,
                "#slot_meta": HomeAttr.GridSlot.META,
                "#grid_slot": grid_slot,
            },
            ExpressionAttributeValues={":item_meta": item_meta},
        )
