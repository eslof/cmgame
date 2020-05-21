from default_imports import *
from tests.test.one import One
from tests.test.two import Two
from tests.test.three import Three


@unique
class TestRequest(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()


# TODO: Update route output (Callable/default=View.generic)
routes = {
    TestRequest.ONE: Route(One, View.debug),
    TestRequest.TWO: Route(Two, View.generic, require_id=False),
    TestRequest.THREE: Route(Three, View.error, require_id=False),
}


@route(routes, TestRequest)
def lambda_handler(event, context):
    pass
