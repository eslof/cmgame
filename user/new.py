from typing import Optional, Any, Dict, no_type_check

from country import Country
from internal import validate_field, end
from properties import RequestField, Constants, ResponseField
from request_handler import RequestHandler
from helper.user_helper import UserHelper


class New(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> dict:
        new_id = UserHelper.new(
            event[RequestField.User.NAME], event[RequestField.User.FLAG]
        )
        if not new_id:
            end("Unable to create new user.")
        return {ResponseField.User.ID: new_id}

    @staticmethod
    @no_type_check
    def validate(event: Dict[str, Any], user_id: Optional[str]):
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
            and value in (val.value for val in Country.__members__.values()),
            message="User New API (FLAG)",
        )
