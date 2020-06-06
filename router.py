import os
from enum import Enum, EnumMeta
from functools import wraps
from typing import Callable, Optional, Any, Dict, Type, no_type_check

from internal import validate_request
from request_handler import RequestHandler
from user_utils import User


class Route:
    def __init__(
        self,
        handler: Type[RequestHandler],
        output: Callable[[Any], str],
        require_id: bool = True,
    ):
        self.handler = handler
        self.output = output
        self.require_id = require_id


ROUTES_TYPE = Dict[Enum, Route]


def _handler(
    routes: ROUTES_TYPE, request_enum: EnumMeta, event: Dict[str, Any],
) -> str:
    _route: Route = routes[validate_request(event, request_enum)]
    user_id: Optional[str] = User.validate_id(event) if _route.require_id else None
    return _route.output(
        _route.handler.run(event, user_id, _route.handler.validate(event, user_id))
    )


# TODO: figure out how we need context
def wrapper(
    routes: ROUTES_TYPE,
    request_enum: EnumMeta,
    f: Callable[[Dict[str, Any], Dict[str, Any]], None],
    event: Dict[str, Any],
) -> str:
    return _handler(routes, request_enum, event)


# Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


def route(
    routes: ROUTES_TYPE, request_enum: EnumMeta
) -> Callable[[Callable[[Dict[str, Any], Any], None]], Callable[..., str]]:
    @no_type_check
    def inner(
        f: Callable[[Dict[str, Any], Dict[str, Any]], None]
    ) -> Callable[..., str]:
        @wraps(f)
        def route_decorated(
            event: Dict[str, Any], context: Optional[Any]
        ) -> Optional[str]:
            os.environ["sourceIP"] = context["identity"]["sourceIP"]
            return wrapper(routes, request_enum, f, event)

        route_decorated.__decorated__ = "route"
        return route_decorated

    return inner
