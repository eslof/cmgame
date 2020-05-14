from internal import RequestHandler, end
from properties import QueueState, UserAttr
from user import User


class Enlist(RequestHandler):
    """User requests to open his home for a possible visitor."""

    @staticmethod
    def run(user_id: str, queue_state: QueueState) -> None:
        """If an enlistment for the given user_id exists then we update its timestamp.
        If there is no enlistment for the given user_id then we add one."""
        if queue_state == QueueState.ENLISTED:
            # TODO: update current listing with new timestamp
            pass
        elif queue_state == QueueState.NONE:
            # TODO: create new listing
            pass
        # TODO: implement
        pass

    @staticmethod
    def validate(user_id: str) -> QueueState:
        queue_state = QueueState(
            User.get(user_id=user_id, attributes=f"{UserAttr.QUEUE_STATE}")
        )
        if queue_state == QueueState.MATCHED:
            end("Queue request API (ENLIST): Currently in a matching.")
        return queue_state
