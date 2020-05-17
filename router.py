from enum import Enum
from typing import Type, Callable
from request_handler import RequestHandler


class Route(object):
    def __init__(self, handler: Type[RequestHandler], output: Callable):
        self.handler = handler
        self.output = output


class Router:
    @staticmethod
    def handle(route: Route, event: dict, user_id: str):
        handler = route.handler
        output = route.output

        user_data = handler.validate(event, user_id)
        output(handler.run(event, user_data, user_id))
