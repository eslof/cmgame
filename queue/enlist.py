from datetime import datetime

from internal import RequestHandler, end
from properties import QueueState, UserAttr
from user import User


class Enlist(RequestHandler):
    """User requests to open his home for a possible visitor."""

    @staticmethod
    def run(user_id: str, queue_state: QueueState) -> bool:
        """If an enlistment for the given user_id exists then we update its timestamp.
        If there is no enlistment for the given user_id then we add one."""
        dt = datetime.today()  # Get timezone naive now
        seconds = int(
            dt.timestamp()
        )  # TODO: this got real annoying real quick SQL is superior
        if queue_state == QueueState.ENLISTED:
            response = table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"SET #meta = :home_meta",
                ConditionExpression=f"attribute_exists(#id)",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#meta": HomeAttr.META,
                },
                ExpressionAttributeValues={":home_meta": meta_data},
            )
            pass
        elif queue_state == QueueState.NONE:
            # TODO: create new listing
            pass
        # TODO: implement
        return True

    @staticmethod
    def validate(user_id: str) -> QueueState:
        queue_state = QueueState(
            User.get(user_id=user_id, attributes=f"{UserAttr.QUEUE_STATE}")
        )
        if queue_state == QueueState.MATCHED:
            end("Queue request API (ENLIST): Currently in a matching.")
        return queue_state
