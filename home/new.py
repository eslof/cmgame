from typing import MappingView, VT_co

from database import UserAttr
from internal import validate_field, end
from properties import RequestField, Constants, Biodome
from request_handler import RequestHandler
from user_utils import User
from .helper.home_helper import HomeHelper
from .helper.user_helper import UserHelper


class New(RequestHandler):
    @staticmethod
    def run(
        event: dict, user_id: str, valid_data: dict, recursion_limit: int = 3
    ) -> bool:
        new_id = HomeHelper.attempt_new()

        if not new_id:
            end("Unable to successfully create new home.")

        return UserHelper.add_home(
            user_id,
            new_id,
            event[RequestField.Home.NAME],
            event[RequestField.Home.BIODOME],
        )

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        user_data = User.get(user_id, UserAttr.HOME_COUNT)
        home_count = user_data[UserAttr.HOME_COUNT]
        if home_count > Constants.User.HOME_COUNT_MAX:
            end("Maximum homes reached")  # TODO: error handling
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
            and value
            in (
                val.value for val in Biodome.__members__.values()
            ),  # type: MappingView[VT_co]
            message="Home Create API (BIODOME)",
        )
        return user_data
