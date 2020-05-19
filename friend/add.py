from typing import Optional, Any
from request_handler import RequestHandler


class Add(RequestHandler):
    """TODO:Add implementation."""

    @staticmethod
    def run(body: dict, user_id: Optional[str], data: Optional[Any]) -> Optional[Any]:
        """TODO:Add.run implementation."""
        pass

    @staticmethod
    def validate(body: dict, user_id: Optional[str]) -> Optional[dict]:
        """TODO:Add.validate implementation."""
        pass
