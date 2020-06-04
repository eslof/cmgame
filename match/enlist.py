from datetime import datetime
from typing import Union, no_type_check

from database import web_socket_endpoint, db_update, db_get
from db_properties import TableKey, TablePartition, UserAttr, MatchAttr
from internal import end
from match.helper.match_helper import MatchHelper
from request_handler import RequestHandler
from user_utils import User


class Enlist(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> Union[bool, str]:
        # todo: more work needed on this
        match_id = valid_data[UserAttr.MATCH_ID]
        if match_id and MatchHelper.get_age(match_id) < 10:  # todo: put in config
            return web_socket_endpoint()["address"]

        new_id = MatchHelper.generate_id(user_id)
        match_id = valid_data[UserAttr.LIST_ID] or MatchHelper.generate_id(user_id)
        results = MatchHelper.update_and_get(match_id, new_id)
        if not results:
            end("Unable to refresh listing.")
        if results["Attributes"][MatchAttr.FINDER_ID]:
            if not User.update(user_id, UserAttr.MATCH_ID, match_id):
                end("Unable to update user with claimed match.")
            return web_socket_endpoint()["address"]
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id):
        user_data = User.get(user_id, f"{UserAttr.LIST_ID}, {UserAttr.MATCH_ID}")
        if not user_data:
            end("Unable to retrieve match id for user.")
        if user_data[UserAttr.LIST_ID]:
            seconds_old = MatchHelper.get_age(user_data[UserAttr.LIST_ID])
            if seconds_old < 4:  # todo: put into config
                end("Attempting to refresh listing too early.")

        return user_data
