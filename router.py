from inspect import isclass
from typing import Callable, Any, Optional
from internal import validate_request, validate_routing
from properties import Constants
from request_handler import RequestHandler
from user import User
from enum import Enum


class Route:
    def __init__(
        self, handler: type(RequestHandler), output: Callable, require_id: bool = False
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


# TODO: collect error messages
def route(routes: dict, request_enum: type(Enum)):
    def inner(f):
        def wrapped_f(*args):
            # region Server (todo: move to unit test)
            assert isclass(
                request_enum
            ), f"Arg request_enum '{request_enum}' is not a class."
            assert (
                f.__name__ == Constants.LAMBDA_HANDLER_NAME
            ), f"Route decorator misuse on '{f.__name__}' for '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}'."
            assert (
                len(args) > 0 and args[0] and type(args[0]) is dict
            ), f"Missing argument in '{Constants.LAMBDA_HANDLER_NAME}' in '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}(event, context)'."
            assert isclass(request_enum), ""
            # endregion

            # region Client
            req = validate_request(args[0], request_enum)
            # endregion

            # region Server (todo: move to unit test)
            validate_routing(routes, request_enum)
            # endregion

            _route = routes[req]
            args = args + (_route,)
            return _handler(*args)

        return wrapped_f

    return inner
