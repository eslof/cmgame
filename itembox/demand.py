from database import UserAttr
from internal import end
from request_handler import RequestHandler
from user_utils import User
from .helper.item_helper import ItemHelper


class Demand(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> list:
        inventory = valid_data[UserAttr.INVENTORY]
        seed = ItemHelper.itembox_seed(
            user_id, valid_data[UserAttr.KEY_COUNT], valid_data[UserAttr.KEY_USED_COUNT]
        )
        return ItemHelper.itembox(3, seed, inventory)

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.INVENTORY}, {UserAttr.KEY_COUNT}, {UserAttr.KEY_USED_COUNT}",
        )
        if user_data[UserAttr.KEY_COUNT] <= 0:
            end(f"Insufficient keys: {user_data[UserAttr.KEY_COUNT]}")

        return user_data
