from enum import unique, auto, Enum
from typing import Dict
from router import Route, route
from view import View
from test.one import One
from test.three import Three
from test.two import Two


@unique
class TestRequest(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()


routes: Dict[Enum, Route] = {
    TestRequest.ONE: Route(One, View.debug),
    TestRequest.TWO: Route(Two, View.generic, require_id=False),
    TestRequest.THREE: Route(Three, View.error, require_id=False),
}


@route(routes, TestRequest)
def lambda_handler(event, context):
    pass
