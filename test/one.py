from typing import Optional, Any

from request_handler import RequestHandler


class One(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: Optional[str], data: Optional[Any]) -> Optional[Any]:
        return data

    @staticmethod
    def validate(event: Any, user_id: Optional[str]) -> Any:
        return event
