from typing import no_type_check

from request_handler import RequestHandler


class List(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data):
        pass

    @staticmethod
    @no_type_check
    def validate(event, user_id):
        pass
