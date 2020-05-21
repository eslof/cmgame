from typing import Optional, Any, Dict

from properties import ResponseField
from request_handler import RequestHandler


class Two(RequestHandler):
    @staticmethod
    def run(event: Dict[str, Any], user_id: Optional[str], data: Any) -> Optional[Any]:
        return data[ResponseField.Generic.RESULT]

    @staticmethod
    def validate(event: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        return event
