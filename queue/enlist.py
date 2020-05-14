from internal import RequestHandler


class Enlist(RequestHandler):
    """User requests to open his home for a possible visitor."""

    @staticmethod
    def run(user_id: str) -> None:
        """If an enlistment for the given user_id exists then we update its timestamp.
        If there is no enlistment for the given user_id then we add one."""
        # TODO: implement
        pass

    @staticmethod
    def validate() -> None:
        """TODO: Not entirely sure what to validate here yet."""
        pass
