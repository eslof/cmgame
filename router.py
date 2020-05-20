from typing import Callable, Optional, Any, Dict, Type
from internal import validate_request
from properties import Constants
from functools import wraps
from request_handler import RequestHandler
from enum import IntEnum

from user import User


class Route:
    def __init__(
        self, handler: type(RequestHandler), output: Callable, require_id: bool = True
    ):
        self.handler = handler
        self.output = output
        self.require_id = require_id


def _handler(routes: Dict[IntEnum, Route], request_enum: Type[IntEnum], event: dict):
    req = validate_request(event, request_enum)
    _route = routes[req]
    user_id = None
    if _route.require_id:
        user_id = User.validate_id(event)
    valid_data = _route.handler.validate(event, user_id)
    output = _route.handler.run(event, user_id, valid_data or None)
    return _route.output(output)


# TODO: figure out how we need context
def wrapper(routes: dict, request_enum: Type[IntEnum], f, *args):
    return _handler(routes, request_enum, args[0])


def route(routes: dict, request_enum: Type[IntEnum]):
    def inner(f):
        @wraps(f)
        def wrapped_f(*args):
            return wrapper(routes, request_enum, f, *args)

        return wrapped_f

    return inner
