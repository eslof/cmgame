from typing import no_type_check

from request_handler import RequestHandler


class Delete(RequestHandler):
    """TODO: User requests to close the user's own account."""

    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> str:
        return ""

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> str:
        return ""
