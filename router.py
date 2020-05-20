from typing import Callable
from internal import validate_request
from properties import Constants
from request_handler import RequestHandler
from enum import Enum


class Route:
    def __init__(
        self, handler: type(RequestHandler), output: Callable, require_id: bool = True
    ):
        self.handler = handler
        self.output = output
        self.require_id = require_id


if __debug__:
    from debug import assert_routing, ROUTE_CLASS

    ROUTE_CLASS = Route


# TODO: collect error messages
def route(routes: dict, request_enum: type(Enum)):
    def inner(f):
        def wrapped_f(*args):
            # region Server (todo: move to unit test)
            if __debug__:
                assert (
                    len(args) > 0 and args[0] and type(args[0]) is dict
                ), f"Missing argument for '{Constants.LAMBDA_HANDLER_NAME}' in '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}(event, context)'."
                assert_routing(f.__name__, routes, request_enum)
            # endregion

            # region Client authoritive (keep this)
            req = validate_request(args[0], request_enum)
            # endregion

            _route = routes[req]
            args = args + (_route,)
            return _handler(*args)

        return wrapped_f

    return inner
