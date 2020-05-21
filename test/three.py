from typing import Optional, Any, Dict

from properties import ResponseField
from request_handler import RequestHandler


class Three(RequestHandler):
    @staticmethod
    def run(event: Dict[str, Any], user_id: Optional[str], data: Any) -> Any:
        return data[ResponseField.Generic.ERROR]

    @staticmethod
    def validate(event: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        return event
