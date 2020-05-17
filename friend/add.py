from typing import Optional, Any

from request_handler import RequestHandler


class Add(RequestHandler):
    """TODO:Add implementation."""

    @staticmethod
    def run(event: dict, user_id: str, data: Any) -> Any:
        """TODO:Add.run implementation."""
        pass

    @staticmethod
    def validate(event: dict, user_id: str) -> Optional[dict]:
        """TODO:Add.validate implementation."""
        pass
