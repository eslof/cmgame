from typing import Optional, Any
from request_handler import RequestHandler


class Clear(RequestHandler):
    """TODO:user request to clear a slot on the grid"""

    @staticmethod
    def run(
        event: dict, user_id: Optional[str], valid_data: Optional[Any]
    ) -> Optional[Any]:
        """TODO:Clear.run implementation."""
        pass

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> Optional[dict]:
        """TODO:Clear.validate implementation."""
        pass
