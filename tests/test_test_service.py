import sys
from typing import Any, Dict
from unittest import TestCase

from db_properties import UserAttr
from internal import generate_id
from properties import (
    PacketHeader,
    RequestField,
    ResponseField,
    ResponseType,
    GameException,
)

test_service_path = "../test"

if test_service_path not in sys.path:
    sys.path.append(test_service_path)
from lambda_function import TestRequest
from lambda_function import lambda_handler

sys.path.remove(test_service_path)
from view import View


class TestTestService(TestCase):
    def setUp(self) -> None:
        self.mock_id = generate_id(UserAttr.SORT_KEY_PREFIX)

    def run_handler(
        self, request: Dict[str, Any], expected_output: Dict[str, Any], test_name: str
    ) -> None:
        output_str: str = lambda_handler(request, None)
        self.assertTrue(output_str, f"{test_name}: None or empty output.")
        expected_str: str = View.serialize(expected_output)
        output_obj: Dict[str, Any] = View.deserialize(output_str)
        self.assertEqual(
            output_str,
            expected_str,
            f"{test_name}: Unexpected output: '{output_str}' should be '{expected_str}'.",
        )
        self.assertEqual(
            output_obj,
            expected_output,
            f"{test_name}: Unexpected output: '{output_obj}' should be '{expected_output}'.",
        )
        print(f"End of integration test using '{test_name}' for test service.")

    def test_debug(self) -> None:
        request = {
            PacketHeader.REQUEST: TestRequest.ONE.value,
            RequestField.User.ID: self.mock_id,
        }
        expected_output = {
            PacketHeader.RESPONSE: ResponseType.DEBUG.value,
            ResponseField.Generic.DEBUG: request,
        }
        self.run_handler(request, expected_output, "View.debug")

    def test_error(self) -> None:
        error_message = "hello world"
        request = {
            PacketHeader.REQUEST: TestRequest.THREE.value,
            ResponseField.Generic.Error.MESSAGE: error_message,
        }
        expected_output = {
            PacketHeader.RESPONSE: ResponseType.ERROR.value,
            ResponseField.Generic.Error.TYPE: GameException.__name__,
            ResponseField.Generic.Error.MESSAGE: error_message,
        }
        self.run_handler(request, expected_output, "View.error")

    def test_generic(self) -> None:
        request = {
            PacketHeader.REQUEST: TestRequest.TWO.value,
            ResponseField.Generic.RESULTS: True,
        }
        expected_output = {
            PacketHeader.RESPONSE: ResponseType.GENERIC.value,
            ResponseField.Generic.RESULTS: request[ResponseField.Generic.RESULTS],
        }
        self.run_handler(request, expected_output, "View.generic")
