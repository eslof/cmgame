from datetime import datetime

from request_handler import RequestHandler
from internal import end
from properties import TableKey, TablePartition, QueueState
from properties import UserAttr, QueueAttr
from user import User
from database import *


class Enlist(RequestHandler):
    """User requests to open his home for a possible visitor."""

    @staticmethod
    def run(user_data: dict, user_id: str) -> bool:
        """If an enlistment for the given user_id exists then we update its timestamp.
        If there is no enlistment for the given user_id then we add one."""
        time = datetime.now().strftime("%d-%H-%M-%S")
        list_id = user_data[UserAttr.LIST_ID]
        new_id = time + user_id
        response = table.update_item(
            Key={TableKey.PARTITION: TablePartition.QUEUE, TableKey.SORT: list_id},
            UpdateExpression="SET #state = :state, #sort = :list_id",
            ExpressionAttributeNames={
                "#state": QueueAttr.STATE,
                "#sort": TableKey.SORT,
            },
            ExpressionAttributeValues={
                ":state": QueueState.ENLISTED.value,
                ":list_id": new_id,
            },
        )
        User.update(user_id, UserAttr.LIST_ID, list_id)
        # TODO: error handling
        return True

    @staticmethod
    def validate(user_id: str) -> QueueState:
        user_data = User.get(
            user_id=user_id, attributes=f"{UserAttr.QUEUE_STATE}, {UserAttr.LIST_ID}",
        )
        queue_state = QueueState(user_data[UserAttr.QUEUE_STATE])
        if queue_state == QueueState.MATCHED:
            end("Queue request API (ENLIST): Currently in a matching.")
        return user_data
