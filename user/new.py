from typing import Optional, Any

from country import Country
from properties import Seed, RequestField, Constants
from internal import validate_field, end
from request_handler import RequestHandler
from .helper.user_helper import UserHelper
from random import Random


class New(RequestHandler):
    """We are blessed with a new user, make sure he has a good time.
    New user is added and receive: A list of starting items and a list of biodomes for a home."""

    @staticmethod
    def run(event: dict, user_id: Optional[str], valid_data: Optional[Any]) -> str:
        new_id = ""
        max_attempts = 5
        while not new_id and max_attempts > 0:
            new_id = UserHelper.attempt_new(
                event[RequestField.User.NAME], event[RequestField.User.FLAG]
            )
            max_attempts -= 1

        if not new_id:
            end("Unable to successfully create new user")

        return new_id

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> None:
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
            and value in Country._value2member_map_,
            message="User New API (FLAG)",
        )
        return None
