from typing import Optional, Any

from request_handler import RequestHandler


class Delete(RequestHandler):
    """User requests to close the user's own account."""

    @staticmethod
    def run(
        event: dict, user_id: Optional[str], valid_data: Optional[Any]
    ) -> Optional[Any]:
        pass

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> Optional[dict]:
        pass
