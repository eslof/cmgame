from internal import RequestHandler, end
from properties import QueueState, UserAttr, TablePartition, TableKey
from user import User


class Find(RequestHandler):
    """User requests to find an enlisted user to visit."""

    @staticmethod
    def run(user_id: str, queue_state: QueueState) -> dict:
        """Find enlistment with a recent timestamp and create a match between enlisted user and given user id."""
        # TODO: look for enlisted other
        response = t(  # table.get_item(
            Key={TableKey.PARTITION: TablePartition.QUEUE},
            ScanIndexForward=False,
            Limit=1,
        )
        listing = response["Item"][0]

        if queue_state == QueueState.ENLISTED:
            # TODO: AND update current listing with new timestamp
            pass
        return {}

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
