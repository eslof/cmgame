from inspect import isclass
from typing import Callable, Any, Optional, Union, List
from internal import validate_request
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


def assert_handler(handler: type):
    assert RequestHandler and isclass(
        RequestHandler
    ), f"Broken or missing RequestHandler base: '{RequestHandler}'."
    assert handler, f"Invalid handler: '{handler}'"
    # TODO: check if we can trick this by deriving
    assert isclass(
        type(handler)
    ), f"Invalid handler: '{handler}' not instance of class."
    assert (
        issubclass(handler, RequestHandler)
        and not (handler is RequestHandler)
        and not (type(handler) is RequestHandler)
    ), f"Invalid inheritance: '{handler}' not derive '{RequestHandler}'."


def assert_route(routes: dict, enum: Enum):
    assert routes[enum], f"Invalid route: '{routes[enum]}' in '{routes}' at '{enum}'."
    assert isinstance(
        routes[enum], Route
    ), f"Invalid route: '{routes[enum]}' not instance of '{Route}' in '{routes}' at '{enum}'."
    assert_handler(routes[enum].handler)
    assert routes[
        enum
    ].output, f"Invalid output: '{routes[enum].output}' for '{routes[enum]}' in '{routes}' at '{enum}'."
    assert callable(
        routes[enum].output
    ), f"Invalid output: '{routes[enum].output}' not callable for '{routes[enum]}' in '{routes}' at '{enum}'."


# todo: move to unit test (?)
def assert_routing(routes: dict, request_enum: type(Enum)):
    assert routes and type(routes) is dict, f"Invalid routes dict: '{routes}'."
    assert (
        request_enum and isclass(request_enum) and len(request_enum)
    ), f"Invalid request_enum: '{request_enum}'"
    for enum in routes:
        assert enum in request_enum, f"Invalid entry: '{enum}' not in '{request_enum}'."
        assert_route(routes, enum)
    for enum in request_enum:
        assert enum in routes, f"Invalid entry: '{enum}' not in '{routes}"
        assert_route(routes, enum)


# TODO: collect error messages
def route(routes: dict, request_enum: type(Enum)):
    def inner(f):
        def wrapped_f(*args):
            # region Server (todo: move to unit test)
            if __debug__:
                assert (
                    f.__name__ == Constants.LAMBDA_HANDLER_NAME
                ), f"Route decorator misuse on '{f.__name__}' for '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}'."
                assert (
                    len(args) > 0 and args[0] and type(args[0]) is dict
                ), f"Missing argument for '{Constants.LAMBDA_HANDLER_NAME}' in '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}(event, context)'."
                assert_routing(routes, request_enum)
            # endregion

            # region Client authoritive (keep this)
            req = validate_request(args[0], request_enum)
            # endregion

            _route = routes[req]
            args = args + (_route,)
            return _handler(*args)

        return wrapped_f

    return inner
