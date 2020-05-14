from internal import RequestHandler


class Find(RequestHandler):
    """User requests to find an enlisted user to visit."""

    @staticmethod
    def run(user_id: str) -> None:
        """Find an enlistment with a recent time-stamp and create a match."""
        # TODO: implement
        pass

    @staticmethod
    def validate() -> None:
        """TODO: Not entirely sure what to validate here yet."""
        pass
