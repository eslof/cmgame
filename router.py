from typing import Callable, Optional, Any
from internal import validate_request
from properties import Constants
from request_handler import RequestHandler
from enum import Enum

from user import User


class Route:
    def __init__(
        self, handler: type(RequestHandler), output: Callable, require_id: bool = True
    ):
        self.handler = handler
        self.output = output
        self.require_id = require_id


def _handler(event: dict, context: Optional[Any], _route: Route):
    """Todo: this is actually part of the model even though it's routing requests... figure something out"""
    user_id = None
    if _route.require_id:
        user_id = User.validate_id(event)
    valid_data = _route.handler.validate(event, user_id)
    output = _route.handler.run(event, user_id, valid_data or None)
    return _route.output(output)


# TODO: figure out a better way to do this
if __debug__:
    from debug import assert_routing


# TODO: collect error messages
def route(routes: dict, request_enum: type(Enum)):
    def inner(f):
        def wrapped_f(*args):
            # region Server (todo: move to unit test)
            if __debug__:
                # TODO: figure out how to actually make this testable
                assert (
                    len(args) > 0 and args[0] and type(args[0]) is dict
                ), f"Missing argument for '{Constants.LAMBDA_HANDLER_NAME}' in '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}(event, context)'."
                assert_routing(f.__name__, routes, request_enum, Route)
            # endregion

            # region Client authoritive (keep this)
            req = validate_request(args[0], request_enum)
            # endregion

            _route = routes[req]
            args = args + (_route,)
            return _handler(*args)

        return wrapped_f

    return inner
