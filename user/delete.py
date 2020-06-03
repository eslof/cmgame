from typing import no_type_check

from internal import end
from request_handler import RequestHandler
from user_utils import User


class Delete(RequestHandler):
    """TODO: CHANGE SORT KEY OF USER ITEM FROM USER TO USERARCHIVE"""

    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        # todo: error handling
        results = User.archive(user_id)
        if not results:
            end("Unable to delete user.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> None:
        return
