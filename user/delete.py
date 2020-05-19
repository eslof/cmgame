from typing import Optional, Any

from request_handler import RequestHandler


class Delete(RequestHandler):
    """User requests to close the user's own account."""

    @staticmethod
    def run(event: dict, user_id: str, data: Any) -> Any:
        pass

    @staticmethod
    def validate(event: dict, user_id: str) -> Optional[dict]:
        pass

    @staticmethod
    def rufn(*args, **kwargs):
        """TODO: research what to do"""
        pass

    @staticmethod
    def valfidate(*args, **kwargs):
        """Validate input phrase for given user_id."""
        pass
