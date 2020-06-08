from typing import no_type_check

from db_properties import UserAttr
from internal import end
from helper.match_helper import MatchHelper
from request_handler import RequestHandler
from user_utils import UserUtils


class Stop(RequestHandler):
    # TODO: implement

    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data):
        list_id = valid_data[UserAttr.LIST_ID]
        if not MatchHelper.delete(list_id):
            end("Unable to delete match listing.")
        if not UserUtils.update(user_id, UserAttr.LIST_ID, ""):
            end("Unable to clear user listing id.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id):
        user_data = UserUtils.get(user_id, UserAttr.LIST_ID)
        if not (user_data and user_data[UserAttr.LIST_ID]):
            end("User not listed.")
        return user_data
