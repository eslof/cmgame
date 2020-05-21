from database import UserAttr
from internal import validate_field
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User
from .helper.home_helper import HomeHelper


class Delete(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> bool:
        home_index = event[RequestField.User.HOME]
        home_id = valid_data[UserAttr.HOMES][home_index]
        HomeHelper.attempt_delete(home_id)
        return User.update(user_id, UserAttr.HOMES, home_index, "REMOVE #name[:value]")

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        user_data = User.get(user_id, UserAttr.HOMES)
        validate_field(
            event,
            RequestField.User.HOME,
            lambda value: type(value) is int
            and 0 < value <= len(user_data[UserAttr.HOMES]),
            "Home delete API",
        )
        return user_data
