from datetime import datetime
from typing import Optional, Any

from database import UserAttr, MatchAttr, web_socket_endpoint
from database import table, TableKey, TablePartition
from internal import end
from properties import Constants
from request_handler import RequestHandler
from user_utils import User


class Enlist(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> Optional[Any]:
        match_id = valid_data[UserAttr.MATCH_ID]
        if match_id:
            table.delete_item(
                Key={
                    TableKey.PARTITION: TablePartition.MATCH,
                    TableKey.SORT: valid_data[UserAttr.MATCH_ID],
                }
            )
            # TODO: send match_id to ws_server to know who to expect
            return web_socket_endpoint()["address"]
        time_now = datetime.now()
        new_id = time_now.strftime("%m-%d-%H-%M-%S") + user_id
        match_id = valid_data[UserAttr.MATCH_ID] or new_id
        # todo: error handling
        table.update_item(
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
        )
        return User.update(user_id, UserAttr.MATCH_ID, new_id)

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        user_data = User.get(user_id, f"{UserAttr.STATE}, {UserAttr.MATCH_ID}")
        time_now = datetime.now()
        if user_data[UserAttr.MATCH_ID]:
            list_time_str = user_data[UserAttr.MATCH_ID][: -Constants.EXPECTED_ID_LEN]
            year_str = time_now.strftime("%Y-")
            list_time = datetime.strptime(
                f"{year_str}{list_time_str}", "%Y-%m-%d-%H-%M-%S"
            )
            listing_age = int((time_now - list_time).total_seconds())
            if listing_age < 1:
                end("Possible misuse, client only runs this once per 5s")

        return user_data
