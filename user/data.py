from typing import Optional, Any

from properties import UserAttr, ResponseField, ItemAttr
from request_handler import RequestHandler
from user import User
from .helper.user_helper import UserHelper
from .helper.item_helper import ItemHelper


class Data(RequestHandler):
    """Returning user requests a welcome package containing: Profile, inventory, home names and their biodomes."""

    @staticmethod
    def run(event: dict, user_id: str, data: Any) -> Any:

        user_data = User.get(user_id, UserHelper.welcome_attributes())
        homes = [
            {
                ResponseField.Home.NAME: home[UserAttr.Home.NAME],
                ResponseField.Home.BIODOME: home[UserAttr.Home.BIODOME],
            }
            for home in user_data[UserAttr.HOMES]
        ]
        inventory = [
            ItemHelper.template_inv(item) for item in user_data[UserAttr.INVENTORY]
        ]
        return UserHelper.template_welcome(user_data, homes, inventory)

    @staticmethod
    def validate(event: dict, user_id: str) -> Optional[dict]:
        pass
