from database import UserAttr
from request_handler import RequestHandler
from user import User
from .helper.user_helper import UserHelper
from .helper.item_helper import ItemHelper


class Data(RequestHandler):
    """Returning user requests a welcome package containing: Profile, inventory, home names and their biodomes."""

    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> dict:
        homes = [
            UserHelper.template_home(
                home[UserAttr.Home.NAME], home[UserAttr.Home.BIODOME]
            )
            for home in data[UserAttr.HOMES]
        ]
        inventory = [ItemHelper.template_inv(item) for item in data[UserAttr.INVENTORY]]
        return UserHelper.template_welcome(data, homes, inventory)

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        return User.get(user_id, UserHelper.welcome_attributes())
