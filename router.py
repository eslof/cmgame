import sys
from inspect import isclass
from typing import Type, Callable, Any, Optional
from internal import validate_request
from properties import Constants
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
    test = sys._getframe().f_code.co_name
    return route.output(output)


def route(routers: dict, request_enum: Type[Enum]):
    def inner(f):
        def wrapped_f(*args):
            assert (
                f.__name__ == Constants.LAMBDA_HANDLER_NAME
            ), f"Route decorator misuse on '{f.__name__}' for '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}'."
            assert (
                len(args) > 0 and args[0] and type(args[0]) is dict
            ), f"Missing argument in '{Constants.LAMBDA_HANDLER_NAME}' in '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}(event, context)'."

            req = validate_request(args[0], request_enum)
            assert req in routers, f"Request '{req}' not present in routers dict."
            _route = routers[req]

            assert isclass(_route) and issubclass(
                _route, Route
            ), f"Value for {req} in routers dict not of class Route"

            args = args + (_route,)
            return lambda_handler(*args)

        return wrapped_f

    return inner
