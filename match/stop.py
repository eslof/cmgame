from request_handler import RequestHandler


class Stop(RequestHandler):
    """User requests to stop his enlistment or search."""

    @staticmethod
    def run(*args, **kwargs):
        """TODO:  Remove listing, change state"""
        pass

    @staticmethod
    def validate(*args, **kwargs):
        """TODO: check if the user is actually in correct state"""
        pass
