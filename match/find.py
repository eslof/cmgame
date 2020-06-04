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
        if match_id:
            return web_socket_endpoint()["address"]

        scan_items = db_scan(
            Key={TableKey.PARTITION: TablePartition.MATCH},
            FilterExpression=Attr(MatchAttr.LISTER_ID).ne(user_id)
            & Attr(MatchAttr.FINDER_ID).eq(""),
            ScanIndexForward=False,
            Limit=1,
        )
        if len(scan_items) == 0:
            return False
        scan_match_id = scan_items[0]["id"]

        seconds_old = MatchHelper.get_age(scan_match_id)
        if seconds_old > 15:
            db_delete(
                Key={
                    TableKey.PARTITION: TablePartition.MATCH,
                    TableKey.SORT: scan_match_id,
                }
            )
            return False

        if not db_update(
            Key={
                TableKey.PARTITION: TablePartition.MATCH,
                TableKey.SORT: scan_match_id,
            },
            UpdateExpression="SET #finder_id = :user_id",
            ConditionExpression=f"attribute_exists(#id) AND #finder_id = :empty",
            ExpressionAttributeValues={":user_id": user_id, ":empty": ""},
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#finder_id": MatchAttr.FINDER_ID,
            },
        ):
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
