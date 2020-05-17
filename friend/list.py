from typing import Optional, Any
from request_handler import RequestHandler


class List(RequestHandler):
    """TODO:get list of friends"""

    @staticmethod
    def run(event: dict, user_id: str, data: Any) -> Any:
        """TODO:List.run implementation."""
        pass

    @staticmethod
    def validate(event: dict, user_id: str) -> Optional[dict]:
        """TODO:List.validate implementation."""
        pass
