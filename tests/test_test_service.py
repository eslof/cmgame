from typing import Any, Dict
from unittest import TestCase

from database import UserAttr
from internal import generate_id
from properties import PacketHeader, RequestField, ResponseField, ResponseType
from test.lambda_function import TestRequest
from test.lambda_function import lambda_handler
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
        self.run_handler(request, expected_output, "debug")

    def test_generic(self) -> None:
        request = {
            PacketHeader.REQUEST: TestRequest.TWO.value,
            ResponseField.Generic.RESULT: True,
        }
        expected_output = {
            PacketHeader.RESPONSE: ResponseType.GENERIC.value,
            ResponseField.Generic.RESULT: request[ResponseField.Generic.RESULT],
        }
        self.run_handler(request, expected_output, "generic")

    def test_error(self) -> None:
        error_message = "hello world"
        request = {
            PacketHeader.REQUEST: TestRequest.THREE.value,
            ResponseField.Generic.ERROR: error_message,
        }
        expected_output = {
            PacketHeader.RESPONSE: ResponseType.ERROR.value,
            ResponseField.Generic.ERROR: request[ResponseField.Generic.ERROR],
        }
        self.run_handler(request, expected_output, "error")
