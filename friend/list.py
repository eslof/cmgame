from typing import Optional, Any
from request_handler import RequestHandler


class List(RequestHandler):
    """TODO:List implementation."""

    @staticmethod
    def run(body: dict, user_id: Optional[str], data: Optional[Any]) -> Optional[Any]:
        """TODO:List.run implementation."""
        pass

    @staticmethod
    def validate(body: dict, user_id: Optional[str]) -> Optional[dict]:
        """TODO:List.validate implementation."""
        pass
