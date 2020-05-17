from typing import Type, Callable
from request_handler import RequestHandler


class Route(object):
    def __init__(self, handler: Type[RequestHandler], output: Callable):
        self.handler = handler
        self.output = output
