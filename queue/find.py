from internal import RequestHandler


class Find(RequestHandler):
    @staticmethod
    def run(user_id: str) -> None:
        # TODO: implement
        pass

    @staticmethod
    def sanitize() -> None:
        # TODO: check if not currently enlisted and/or in find state?
        pass
