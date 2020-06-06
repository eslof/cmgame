from typing import Union, no_type_check

from db_properties import UserAttr, MatchAttr
from internal import end, web_socket_endpoint
from match.helper.match_helper import MatchHelper
from request_handler import RequestHandler
from user_utils import User


class Enlist(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> Union[bool, str]:
        match_id = valid_data[UserAttr.MATCH_ID]
        if match_id and MatchHelper.get_age(match_id) < 10:  # todo: put in config
            return web_socket_endpoint()["address"]
        list_id = valid_data[UserAttr.LIST_ID]
        if not list_id:
            new_id = MatchHelper.generate_id(user_id)
            if not MatchHelper.new(new_id, user_id):
                end("Unable to create match listing.")
            if not User.update(user_id, UserAttr.LIST_ID, new_id):
                end("Unable to update user listing id.")
            return True

        new_id = MatchHelper.generate_id(user_id)
        results = MatchHelper.upsert_return(list_id, new_id)
        if not results:
            end("Unable to refresh listing.")
        if MatchAttr.FINDER_ID in results.get("Attributes", {}):
            return True
        if not User.update(user_id, UserAttr.MATCH_ID, new_id):
            end("Unable to update user with claimed match.")
        return web_socket_endpoint()["address"]

    @staticmethod
    @no_type_check
    def validate(event, user_id):
        user_data = User.get(user_id, f"{UserAttr.LIST_ID}, {UserAttr.MATCH_ID}")
        if not user_data:
            end("Unable to retrieve match and listing for user.")
        if user_data[UserAttr.LIST_ID]:
            seconds_old = MatchHelper.get_age(user_data[UserAttr.LIST_ID])
            if seconds_old < 2.5:  # todo: put into config
                end("Attempting to refresh listing too early.")

        return user_data
