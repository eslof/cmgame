from typing import Optional, Any, Dict

from request_handler import RequestHandler


class One(RequestHandler):
    @staticmethod
    def run(event: Dict[str, Any], user_id: Optional[str], data: Any) -> Optional[Any]:
        return data

    @staticmethod
    def validate(event: Dict[str, Any], user_id: Optional[str]) -> Dict[str, Any]:
        return event
