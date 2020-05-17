from .helper.home_helper import HomeHelper
from database import UserAttr
from internal import validate_field, end
from properties import RequestField, Constants, Biodome
from request_handler import RequestHandler
from user import User


class New(RequestHandler):
    """User requests to create a new home."""

    @staticmethod
    def run(event: dict, user_id: str, data: dict, recursion_limit: int = 3) -> str:
        """TODO: this entire thing needs a rework: there need be a template for user item
        TODO: should it be recursive or is there a better way?"""
        new_id = None
        max_attempts = 5
        while not new_id and max_attempts > 0:
            new_id = HomeHelper.attempt_new()
            max_attempts -= 1

        if not new_id:
            end("Unable to successfully create new home")

        return User.add_home(
            user_id, UserAttr.HOMES, home_index, "REMOVE #name[:value]"
        )

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        """Confirm name to be of appropriate length, and existence of requested Biodome."""
        user_data = User.get(user_id, UserAttr.HOMES)
        home_count = len(user_data[UserAttr.HOMES])
        if home_count > Constants.User.HOME_COUNT_MAX:
            end("Maximum homes reached")  # TODO: error handling
        validate_field(
            target=event,
            field=RequestField.Home.NAME,
            validation=lambda value: isinstance(value, str)
            and 0 < len(value) <= Constants.Home.NAME_MAX_LENGTH,
            message="Home Create API (NAME)",
        )
        validate_field(
            target=event,
            field=RequestField.Home.BIODOME,
            validation=lambda value: isinstance(value, int)
            and value in Biodome._value2member_map_,
            message="Home Create API (BIODOME)",
        )
        return user_data
