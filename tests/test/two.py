from typing import Optional, Any

from properties import ResponseField
from request_handler import RequestHandler


class Two(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: Optional[str], data: Optional[Any]) -> Optional[Any]:
        return data[ResponseField.Generic.RESULT]

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> Optional[dict]:
        return event
