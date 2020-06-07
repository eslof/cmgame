from typing import Dict, no_type_check

from Config import Config
from db_properties import UserAttr
from home.helper.home_helper import HomeHelper
from home.helper.user_helper import UserHelper
from internal import validate_field, end
from properties import RequestField, Constants
from request_handler import RequestHandler
from user_utils import User


class New(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        new_id = HomeHelper.new()
        if not new_id:
            end("Unable to create new home.")
        # TODO: delete home if add_home fails
        if not UserHelper.add_home(
            user_id,
            new_id,
            event[RequestField.Home.NAME],
            event[RequestField.Home.BIODOME],
        ):
            if not HomeHelper.delete(new_id):
                end("Unable to add home to user, and failed clean-up.")
            end("Unable to add home to user.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, int]:
        user_data = User.get(user_id, UserAttr.HOME_COUNT)
        if not user_data:
            end("Unable to retrieve home count for user.")
        if user_data[UserAttr.HOME_COUNT] >= Constants.User.HOME_COUNT_MAX:
            end("Maximum homes reached.")
        validate_field(
            target=event,
            field=RequestField.Home.NAME,
            validation=lambda value: type(value) is str
            and 0 < len(value) <= Constants.Home.NAME_MAX_LENGTH,
            message="Home Create API (NAME)",
        )
        validate_field(
            target=event,
            field=RequestField.Home.BIODOME,
            validation=lambda value: type(value) is int
            and 1 <= value <= Config.BIODOME_COUNT,
            message="Home Create API (BIODOME)",
        )
        return user_data
