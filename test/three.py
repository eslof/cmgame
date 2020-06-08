from typing import Any, Dict, no_type_check

from properties import ResponseField
from request_handler import RequestHandler


class Three(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> Dict[str, Any]:
        return valid_data[ResponseField.Generic.Error.MESSAGE]

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Any]:
        return event
