from typing import no_type_check

from request_handler import RequestHandler


class Delete(RequestHandler):
    """TODO: Figure out how we do this proper without just losing data."""

    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> str:
        return ""

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> str:
        return ""
