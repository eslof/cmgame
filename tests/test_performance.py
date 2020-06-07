from typing import Any, Dict
from time import perf_counter
from db_properties import UserAttr
from internal import generate_id
from properties import (
    PacketHeader,
    RequestField,
    ResponseField,
)
from test.lambda_function import TestRequest
from test.lambda_function import lambda_handler

mock_id = generate_id(UserAttr.SORT_KEY_PREFIX)
debug_request = {
    PacketHeader.REQUEST: TestRequest.ONE.value,
    RequestField.User.ID: mock_id,
}
debug_name = "test.one:View.debug"
error_message = "hello world"
error_request = {
    PacketHeader.REQUEST: TestRequest.THREE.value,
    ResponseField.Generic.ERROR_MESSAGE: error_message,
}
error_name = "test.three:View.error"
generic_request = {
    PacketHeader.REQUEST: TestRequest.TWO.value,
    ResponseField.Generic.RESULTS: True,
}
generic_name = "test.two:View.generic"
test_range = range(100000)


class TestPerformance:
    alive: str = ""

    @classmethod
    def run_handler(cls, request: Dict[str, Any], test_name: str) -> None:
        t_ = perf_counter()
        output_str: str = lambda_handler(request, None)
        end = perf_counter()
        cls.alive = output_str
        t__ = perf_counter()
        for _ in test_range:
            output_str: str = lambda_handler(request, None)
        _end = perf_counter()
        print(
            f"'{test_name}'\t:\tsingle {((end-t_)*1000000):.1f}µs\tx100k {_end-t__:.3f}s"
        )
        cls.alive = output_str

    @classmethod
    def test_debug(cls) -> None:
        cls.run_handler(debug_request, debug_name)

    @classmethod
    def test_error(cls) -> None:
        cls.run_handler(error_request, error_name)

    @classmethod
    def test_generic(cls) -> None:
        cls.run_handler(generic_request, generic_name)

    @classmethod
    def test_z(cls) -> None:
        cls.run_handler(debug_request, debug_name)
        cls.run_handler(error_request, error_name)
        cls.run_handler(generic_request, generic_name)


TestPerformance.test_z()
print()
TestPerformance.test_z()
print("\nIt's all ogre now.")
