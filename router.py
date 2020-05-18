from typing import Type, Callable, Any, Optional
from internal import validate_request
from request_handler import RequestHandler
from user import User
from enum import Enum


class Route(object):
    def __init__(
        self, handler: Type[RequestHandler], output: Callable, require_id: bool = False
    ):
        self.handler = handler
        self.output = output
        self.require_id = require_id


def lambda_handler(event: dict, context: Optional[Any], route: Route):
    """Todo: this is actually part of the model even though it's routing requests... figure something out"""
    user_id = None
    if route.require_id:
        user_id = User.validate_id(event)
    valid_data = route.handler.validate(event, user_id)
    output = route.handler.run(event, user_id, valid_data or None)
    return route.output(output)


def route(routers: dict, request_enum: Type[Enum]):
    def inner(f):
        def wrapped_f(*args):
            req = validate_request(args[0], request_enum)
            args = args + (routers[req])
            return lambda_handler(*args)

        return wrapped_f

    return inner
