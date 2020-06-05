from typing import no_type_check, Dict, Union

from boto3.dynamodb.conditions import Attr

from database import web_socket_endpoint, db_scan, db_update, db_delete
from db_properties import UserAttr, TablePartition, TableKey, MatchAttr
from internal import end
from match.helper.match_helper import MatchHelper
from request_handler import RequestHandler
from user_utils import User


class Find(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data: Dict[str, str]) -> Union[str, bool]:
        match_id = valid_data[UserAttr.MATCH_ID]
        if (
            match_id
            and MatchHelper.get_age(match_id) < 10  # todo: Constants.MATCH_COOLDOWN
        ):
            return web_socket_endpoint()["address"]
        scan_items = MatchHelper.find_available(user_id)
        if not scan_items:
            return False
        scan_match_id = scan_items[0]["id"]

        seconds_old = MatchHelper.get_age(scan_match_id)
        if seconds_old > 15:
            MatchHelper.delete(scan_match_id)
            return False

        if not MatchHelper.claim(scan_match_id, user_id):
            return False

        if not User.update(user_id, UserAttr.MATCH_ID, scan_match_id):
            end("Unable to update user match id.")
        # todo: send match id to chat server to expect lister_id and finder_id
        return web_socket_endpoint()["address"]

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, str]:
        user_data = User.get(user_id, UserAttr.MATCH_ID)
        return user_data
