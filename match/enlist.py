from datetime import datetime
from typing import Optional, Any

from database import (
    table,
    TableKey,
    TablePartition,
    UserAttr,
    MatchAttr,
    web_socket_endpoint,
)
from internal import end
from properties import MatchState, UserState, Constants
from request_handler import RequestHandler
from user import User


class Enlist(RequestHandler):
    """User requests to open his home for a possible visitor."""

    @staticmethod
    def run(event: dict, user_id: str, data: dict) -> Optional[Any]:
        """If an enlistment for the given user_id exists then we update its timestamp.
        If there is no enlistment for the given user_id then we add one."""
        match_id = UserState(data[UserAttr.MATCH_ID])
        # todo: just get queue ID instead
        if match_id:
            table.delete_item(
                Key={
                    TableKey.PARTITION: TablePartition.MATCH,
                    TableKey.SORT: data[UserAttr.MATCH_ID],
                }
            )
            # TODO: send match_id to ws_server to know who to expect
            return web_socket_endpoint()["address"]
        time_now = datetime.now()
        new_id = time_now.strftime("%m-%d-%H-%M-%S") + user_id
        match_id = data[UserAttr.MATCH_ID] or new_id
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
        # TODO: check if MATCH_ID is empty to determine if user is enlisted
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
