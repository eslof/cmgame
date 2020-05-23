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
routes: ROUTES_TYPE = {
    TestRequest.ONE: Route(One, View.debug),
    TestRequest.TWO: Route(Two, View.generic, require_id=False),
    TestRequest.THREE: Route(Three, View.error, require_id=False),
}


@route(routes, TestRequest)
def lambda_handler(event: Dict[str, Any], context: Any) -> str:
    pass
