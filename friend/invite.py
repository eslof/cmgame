from typing import Optional, Any
from request_handler import RequestHandler


class Invite(RequestHandler):
    """TODO:Invite implementation."""

    @staticmethod
    def run(event: dict, user_id: Optional[str], data: Optional[Any]) -> Optional[Any]:
        """TODO:Invite.run implementation."""
        pass

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> Optional[dict]:
        """TODO:Invite.validate implementation."""
        pass
