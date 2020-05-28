from typing import no_type_check, Dict, Any

from database import UserAttr
from internal import validate_field
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User
from .helper.home_helper import HomeHelper


class Delete(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        home_index = event[RequestField.User.HOME] - 1
        home_id = valid_data[UserAttr.HOMES][home_index]
        HomeHelper.attempt_delete(home_id)
        # todo: do we need an extra if :value in #name condition here to catch misuse?
        return User.update(user_id, UserAttr.HOMES, home_index, "REMOVE #name :value")

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Any]:
        user_data = User.get(user_id, UserAttr.HOMES)
        validate_field(
            event,
            RequestField.User.HOME,
            lambda value: type(value) is int
            and 0 < value <= len(user_data[UserAttr.HOMES]),
            "Home delete API",
        )
        return user_data
