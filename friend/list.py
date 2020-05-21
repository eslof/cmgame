from typing import Optional, Any

from request_handler import RequestHandler


class List(RequestHandler):
    @staticmethod
    def run(
        event: dict, user_id: Optional[str], valid_data: Optional[Any]
    ) -> Optional[Any]:
        pass

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> Optional[dict]:
        pass
