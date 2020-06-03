from typing import no_type_check, Dict, Any

from db_properties import UserAttr
from internal import validate_field, end
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
        if not HomeHelper.delete(home_id):
            end("Unable to delete requested home.")
        # todo: do we need an extra if :value in #name condition here to catch misuse?
        if not User.update(user_id, UserAttr.HOMES, home_index, "REMOVE #name :value"):
            end("Unable to remove deleted home from user.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Any]:
        user_data = User.get(user_id, UserAttr.HOMES)
        if not user_data:
            end("Unable to retrieve homes list for user.")
        validate_field(
            event,
            RequestField.User.HOME,
            lambda value: type(value) is int
            and 0 < value <= len(user_data[UserAttr.HOMES]),
            "Home delete API",
        )
        return user_data
