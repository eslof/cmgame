from request_handler import RequestHandler
from internal import end
from properties import QueueState, UserAttr, TablePartition, TableKey
from user import User
from database import *


class Find(RequestHandler):
    """User requests to find an enlisted user to visit."""

    @staticmethod
    def run(user_id: str, queue_state: QueueState) -> dict:
        """Find enlistment with a recent timestamp and create a match between enlisted user and given user id."""
        # TODO: look for enlisted other
        response = table.get_item(
            Key={TableKey.PARTITION: TablePartition.QUEUE},
            # TODO: condition expression: state != matched
            ScanIndexForward=False,
            Limit=1,
        )
        listing = None
        if len(response["Item"] > 0):
            listing = response["Item"][0]
            # TODO: update listing's state to matched, and prompt for accept by finder
            # TODO: then as the enlisters code comes to update its enlistment we look for this
        elif queue_state == QueueState.ENLISTED:
            # TODO: So you can't be enlisted and find at the same time but they can both override eachother
            # TODO: so figure that part out...
            pass
        return listing

    @staticmethod
    def validate(user_id: str) -> QueueState:
        """Get and return queue state for given user id.
        Confirm queue state not to be already matched."""
        queue_state = QueueState(
            User.get(user_id=user_id, attributes=f"{UserAttr.QUEUE_STATE}")
        )
        if queue_state == QueueState.MATCHED:
            end("Queue request API (ENLIST): Currently in a matching.")
        return queue_state
