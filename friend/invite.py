from typing import Optional, Any
from request_handler import RequestHandler


class Invite(RequestHandler):
    """TODO:invite player"""

    @staticmethod
    def run(event: dict, user_id: str, data: Any) -> Any:
        """TODO:Invite.run implementation."""
        pass

    @staticmethod
    def validate(event: dict, user_id: str) -> Optional[dict]:
        """TODO:Invite.validate implementation."""
        pass
