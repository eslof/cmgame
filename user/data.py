from typing import Dict, Any, Optional, Union, List, no_type_check

from database import UserAttr
from request_handler import RequestHandler
from user_utils import User
from .helper.item_helper import ItemHelper
from .helper.user_helper import UserHelper


class Data(RequestHandler):
    """Returning user requests a welcome package containing: Profile, inventory, home names and their biodomes."""

    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> Dict[str, Any]:
        homes: List[Dict[str, Union[str, int]]] = [
            UserHelper.template_home(
                home[UserAttr.Home.NAME], home[UserAttr.Home.BIODOME]
            )
            for home in valid_data[UserAttr.HOMES]
        ]
        inventory = [
            ItemHelper.template_inv(item) for item in valid_data[UserAttr.INVENTORY]
        ]
        return UserHelper.template_welcome(valid_data, homes, inventory)

    @staticmethod
    @no_type_check
    def validate(event: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        return User.get(user_id, UserHelper.welcome_attributes())
