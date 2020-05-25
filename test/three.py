from typing import Any, Dict, no_type_check

from properties import ResponseField
from request_handler import RequestHandler


class Three(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, data) -> Dict[str, Any]:
        return data[ResponseField.Generic.ERROR]

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, Any]:
        return event
