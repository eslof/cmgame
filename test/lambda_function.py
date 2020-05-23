import inspect
from enum import unique, auto, Enum
from typing import Dict, Any

from router import Route, ROUTES_TYPE, route
from test.one import One
from test.three import Three
from test.two import Two
from view import View


@unique
class TestRequest(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()


# TODO: Update route output (Callable/default=View.generic)
routes: Dict[Enum, Route] = {
    TestRequest.ONE: Route(One, View.debug),
    TestRequest.TWO: Route(Two, View.generic, require_id=False),
    TestRequest.THREE: Route(Three, View.error, require_id=False),
}


# print(TestRequest.ONE in routes.__annotations__[routes.__name][0])


@route(routes, TestRequest)
def lambda_handler(event: Dict[str, Any], context: Any) -> str:
    pass
