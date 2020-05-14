from internal import RequestHandler


class Enlist(RequestHandler):
    """User requests to open his home for a possible visitor."""

    @staticmethod
    def run(user_id: str) -> None:
        """If the user already has an enlistment then we update its timestamp.
        If the user has no enlistment then we add an enlistment entry for this user."""
        # TODO: implement
        pass

    @staticmethod
    def validate() -> None:
        """TODO: Not entirely sure what to validate here yet."""
        pass
