from datetime import datetime
from typing import Optional, Any

from database import table, TableKey, TablePartition, UserAttr, QueueAttr
from internal import end
from properties import QueueState, UserState, Constants
from request_handler import RequestHandler
from user import User


class Enlist(RequestHandler):
    """User requests to open his home for a possible visitor."""

    @staticmethod
    def run(event: dict, user_id: str, data: dict) -> Optional[Any]:
        """If an enlistment for the given user_id exists then we update its timestamp.
        If there is no enlistment for the given user_id then we add one."""
        time_now = datetime.now()
        new_id = time_now.strftime("%m-%d-%H-%M-%S") + user_id
        list_id = data[UserAttr.QUEUE_ID] or new_id

        response = table.update_item(
            Key={TableKey.PARTITION: TablePartition.QUEUE, TableKey.SORT: list_id},
            UpdateExpression="SET #state = :state, #sort = :list_id",
            ExpressionAttributeNames={
                "#state": QueueAttr.STATE,
                "#sort": TableKey.SORT,
            },
            ExpressionAttributeValues={
                ":state": QueueState.NORMAL.value,
                ":list_id": new_id,
            },
        )
        return User.update(user_id, UserAttr.QUEUE_ID, list_id)

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        # TODO: check if QUEUE_ID is empty to determine if user is enlisted
        user_data = User.get(user_id, f"{UserAttr.STATE}, {UserAttr.QUEUE_ID}")
        user_state = UserState(user_data[UserAttr.STATE])
        if user_state == UserState.MATCHED:
            end("Queue request API (ENLIST): Currently in a matching.")

        time_now = datetime.now()

        if user_data[UserAttr.QUEUE_ID]:
            list_time_str = user_data[UserAttr.QUEUE_ID][: -Constants.EXPECTED_ID_LEN]
            year_str = time_now.strftime("%Y-")
            list_time = datetime.strptime(
                f"{year_str}{list_time_str}", "%Y-%m-%d-%H-%M-%S"
            )
            listing_age = int((time_now - list_time).total_seconds())
            if listing_age < 1:
                end("Possible misuse, client only runs this once per 5s")

        return user_data
