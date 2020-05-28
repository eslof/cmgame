from typing import Dict, no_type_check

from database import UserAttr
from internal import validate_field, end
from properties import RequestField, Constants, Biodome
from request_handler import RequestHandler
from user_utils import User
from home.helper.home_helper import HomeHelper
from home.helper.user_helper import UserHelper


class New(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        new_id = HomeHelper.attempt_new()

        return UserHelper.add_home(
            user_id,
            new_id,
            event[RequestField.Home.NAME],
            event[RequestField.Home.BIODOME],
        )

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, int]:
        user_data = User.get(user_id, UserAttr.HOME_COUNT)
        home_count = user_data[UserAttr.HOME_COUNT]
        if home_count > Constants.User.HOME_COUNT_MAX:
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
            and value in (val.value for val in Biodome.__members__.values()),
            message="Home Create API (BIODOME)",
        )
        return user_data
