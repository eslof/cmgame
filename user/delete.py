from typing import no_type_check

from internal import end
from request_handler import RequestHandler
from user.helper.user_helper import UserHelper


class Delete(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        if not UserHelper.archive(user_id):
            end("Unable to delete user.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> None:
        return
