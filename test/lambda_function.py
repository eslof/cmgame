from enum import unique, auto, Enum
from typing import Dict

from router import Route, route
from one import One
from three import Three
from two import Two
from view import View


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
def lambda_handler(event, context):  # noqa
    pass
