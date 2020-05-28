from typing import Optional, Any, Dict, no_type_check

from country import Country
from internal import validate_field, end
from properties import RequestField, Constants, ResponseField
from request_handler import RequestHandler
from .helper.item_helper import ItemHelper
from .helper.user_helper import UserHelper


class New(RequestHandler):
    """We are blessed with a new user, make sure he has a good time.
    New user is added and receive: A list of starting items, a list of biodomes for a home, and his ID/token."""

    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> dict:
        new_id = UserHelper.attempt_new(
            event[RequestField.User.NAME], event[RequestField.User.FLAG]
        )

        return {
            ResponseField.User.ID: new_id,
            ResponseField.User.WELCOME: ItemHelper.welcome_info(),
        }

    @staticmethod
    @no_type_check
    def validate(event: Dict[str, Any], user_id: Optional[str]):
        validate_field(
            target=event,
            field=RequestField.User.NAME,
            validation=lambda value: type(value) is str
            and 0 < len(value) < Constants.User.NAME_MAX_LENGTH,
            message="User New API (NAME)",
        )
        validate_field(
            target=event,
            field=RequestField.User.FLAG,
            validation=lambda value: type(value) is int
            and value in (val.value for val in Country.__members__.values()),
            message="User New API (FLAG)",
        )
