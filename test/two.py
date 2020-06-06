from typing import Any, Dict, no_type_check

from properties import ResponseField
from request_handler import RequestHandler


class Two(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        return valid_data[ResponseField.Generic.RESULTS]

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Any]:
        return event
