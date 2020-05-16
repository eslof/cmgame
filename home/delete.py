from request_handler import RequestHandler
from internal import validate_field
from properties import UserAttr, RequestField, Constants
from user import User
from database import *

# TODO: research maybe using glacier to store deleted entries?
#   although it really doesn't matter since homes can be freely replicated at no expense
class Delete(RequestHandler):
    """Delete documentation"""

    @staticmethod
    def run(event: dict, user_data: dict, user_id: str) -> bool:
        """Run documentation TODO: stuff"""
        homes = user_data[UserAttr.HOMES]
        del homes[event[RequestField.User.HOME_INDEX]]
        User.update(user_id, UserAttr.HOMES, set(homes))
        pass

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        """User.get HOMES """
        user_data = User.get(user_id, UserAttr.HOMES)
        validate_field(
            event,
            RequestField.User.HOME_INDEX,
            lambda value: isinstance(value, int)
            and 0 < value <= len(user_data[UserAttr.HOMES]),
            "Home delete API",
        )
        return user_data
