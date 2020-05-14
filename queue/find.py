from internal import RequestHandler


class Find(RequestHandler):
    """User requests to find an enlisted user to visit."""

    @staticmethod
    def run(user_id: str) -> None:
        """Find enlistment with a recent timestamp and create a match between enlisted user and given user id."""
        # TODO: implement
        pass

    @staticmethod
    def validate() -> None:
        """TODO: Not entirely sure what to validate here yet."""
        pass
