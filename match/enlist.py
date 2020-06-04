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
        if match_id:
            results = db_get(
                Key={
                    TableKey.PARTITION: TablePartition.MATCH,
                    TableKey.SORT: valid_data[UserAttr.MATCH_ID],
                },
                ProjectionExpression=MatchAttr.FINDER_ID,
            )
            if not (results and "Item" in results and results["Item"]):
                end("Current matching not found.")
            if results["Item"][0][MatchAttr.FINDER_ID]:
                return web_socket_endpoint()["address"]
        time_now = datetime.now()
        new_id = time_now.strftime("%m-%d-%H-%M-%S") + user_id
        match_id = valid_data[UserAttr.MATCH_ID] or new_id
        results = db_update(
            Key={TableKey.PARTITION: TablePartition.MATCH, TableKey.SORT: match_id},
            UpdateExpression="SET #sort = :new_match_id, #lister_id = :",
            ExpressionAttributeNames={
                "#lister_id": MatchAttr.LISTER_ID,
                "#finder_id": MatchAttr.FINDER_ID,
                "#sort": TableKey.SORT,
            },
            ExpressionAttributeValues={
                ":new_match_id": new_id,
                ":user_id": user_id,
                ":other_id": "",
            },
            ReturnValues="ALL_NEW",
        )
        if not results:
            end("Unable to refresh listing.")
        finder_id = results["Attributes"][MatchAttr.FINDER_ID]
        results = User.update(user_id, UserAttr.LIST_ID, new_id)
        if not results:
            end("Unable to update users match id.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id):
        user_data = User.get(user_id, f"{UserAttr.MATCH_ID}")
        if not user_data:
            end("Unable to retrieve match id for user.")
        if user_data[UserAttr.MATCH_ID]:
            seconds_old = MatchHelper.get_age(user_data[UserAttr.MATCH_ID])
            if seconds_old < 4:  # todo: put into config
                end("Attempting to refresh listing too early.")

        return user_data
