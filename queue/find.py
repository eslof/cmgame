from typing import Optional, Any, Union

from database import *
from internal import end
from properties import QueueState
from request_handler import RequestHandler
from user import User


class Find(RequestHandler):
    """User requests to find an enlisted user to visit."""

    @staticmethod
    def run(event: dict, user_id: str, data: dict) -> Union[str, bool]:
        queue_state = QueueState(data[UserAttr.QUEUE_STATE])
        if queue_state == QueueState.MATCHED:
            return web_socket_endpoint()["address"]
        response = table.get_item(
            Key={TableKey.PARTITION: TablePartition.QUEUE},
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
        # TODO: error handling
        if len(response["Item"] > 0):
            # TODO: update listing's state to pending, and prompt for accept by finder
            # TODO: then as the enlisters code comes to update its enlistment we look for this

            return web_socket_endpoint()["address"]
        return False

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> dict:
        """Get and return queue state for given user id.
        Confirm queue state not to be already matched."""
        user_data = User.get(user_id, UserAttr.QUEUE_STATE)
        return user_data
