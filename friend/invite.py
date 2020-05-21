from typing import Optional, Any

from request_handler import RequestHandler


class Invite(RequestHandler):
    @staticmethod
    def run(
        event: dict, user_id: Optional[str], valid_data: Optional[Any]
    ) -> Optional[Any]:
        return event

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> Optional[dict]:
        return event
