from .helper.home_helper import HomeHelper
from database import UserAttr
from internal import validate_field
from properties import RequestField
from request_handler import RequestHandler
from user import User


# TODO: research maybe using glacier to store deleted entries?
#   although it really doesn't matter since homes can be freely replicated at no expense
class Delete(RequestHandler):
    """Delete documentation"""

    @staticmethod
    def run(body: dict, user_id: str, data: dict) -> bool:
        """Run documentation TODO: stuff"""
        home_index = body[RequestField.User.HOME]
        home_id = data[UserAttr.HOMES][home_index]
        HomeHelper.attempt_delete(home_id)
        return User.update(user_id, UserAttr.HOMES, home_index, "REMOVE #name[:value]")

    @staticmethod
    def validate(body: dict, user_id: str) -> dict:
        """User.get HOMES """
        user_data = User.get(user_id, UserAttr.HOMES)
        validate_field(
            body,
            RequestField.User.HOME,
            lambda value: isinstance(value, int)
            and 0 < value <= len(user_data[UserAttr.HOMES]),
            "Home delete API",
        )
        return user_data
