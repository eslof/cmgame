from typing import Optional, Any
from request_handler import RequestHandler


class List(RequestHandler):
    """TODO:List implementation."""

    @staticmethod
    def run(
        event: dict, user_id: Optional[str], valid_data: Optional[Any]
    ) -> Optional[Any]:
        """TODO:List.run implementation."""
        pass

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> Optional[dict]:
        """TODO:List.validate implementation."""
        pass
