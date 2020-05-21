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
    ) -> str:
        new_id = None
        max_attempts = 5
        while not new_id and max_attempts > 0:
            new_id = HomeHelper.attempt_new()
            max_attempts -= 1

        if not new_id:
            end("Unable to successfully create new home")

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
            and value in Biodome._value2member_map_,
            message="Home Create API (BIODOME)",
        )
        return user_data
