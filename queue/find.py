from request_handler import RequestHandler
from internal import end
from properties import QueueState, UserAttr, TablePartition, TableKey, QueueAttr
from user import User
from database import *


class Find(RequestHandler):
    """User requests to find an enlisted user to visit."""

    @staticmethod
    def run(user_data: str, user_id: str) -> dict:
        """Find enlistment with a recent timestamp and create a match between enlisted user and given user id."""
        # TODO: look for enlisted other
        response = table.get_item(
            Key={TableKey.PARTITION: TablePartition.QUEUE},
            IndexName="date",
            # TODO: condition expression: state != matched
            ConditionExpression="#state <> :matched AND #enlisted_id <> :finder_id",
            ExpressionAttributeNames={
                "#state": QueueAttr.STATE,
                "#enlisted_id": QueueAttr.USER_ID,
            },
            ExpressionAttributeValues={
                ":matched": QueueState.MATCHED.value,
                ":finder_id": user_id,
            },
            ScanIndexForward=False,
            Limit=1,
        )
        listing = None
        if len(response["Item"] > 0):
            listing = response["Item"][0]
            # TODO: update listing's state to matched, and prompt for accept by finder
            # TODO: then as the enlisters code comes to update its enlistment we look for this
        else:
            return {}
        return listing

    @staticmethod
    def validate(user_id: str) -> QueueState:
        """Get and return queue state for given user id.
        Confirm queue state not to be already matched."""
        user_data = User.get(user_id, UserAttr.QUEUE_STATE)
        queue_state = QueueState(user_data[UserAttr.QUEUE_STATE])
        if queue_state == QueueState.MATCHED:
            end("Queue request API (ENLIST): Currently in a matching.")
        return user_data
