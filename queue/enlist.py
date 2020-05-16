from datetime import datetime

from internal import RequestHandler, end
from properties import TableKey, TablePartition, QueueState
from properties import UserAttr, QueueAttr
from user import User
from database import *


class Enlist(RequestHandler):
    """User requests to open his home for a possible visitor."""

    @staticmethod
    def run(user_id: str, queue_state: QueueState) -> bool:
        """If an enlistment for the given user_id exists then we update its timestamp.
        If there is no enlistment for the given user_id then we add one."""
        dt = datetime.today()  # Get timezone naive now
        seconds = int(dt.timestamp())
        response = table.update_item(
            Key={TableKey.PARTITION: TablePartition.QUEUE, TableKey.SORT: user_id},
            UpdateExpression=f"SET #date = :seconds",
            ExpressionAttributeNames={"#date": QueueAttr.DATE},
            ExpressionAttributeValues={":seconds": seconds},
        )
        # TODO: error handling
        return True

    @staticmethod
    def validate(user_id: str) -> QueueState:
        queue_state = QueueState(
            User.get(user_id=user_id, attributes=f"{UserAttr.QUEUE_STATE}")
        )
        if queue_state == QueueState.MATCHED:
            end("Queue request API (ENLIST): Currently in a matching.")
        return queue_state
