from typing import Any, Dict, Optional
from unittest import TestCase

from database import UserAttr
from internal import generate_id
from properties import PacketHeader, RequestField, ResponseField, ResponseType
from test.lambda_function import TestRequest
from test.lambda_function import lambda_handler
from view import View


class TestService(TestCase):
    mock_id = generate_id(UserAttr.SORT_KEY_PREFIX)

    def run_handler(
        self, mock: Dict[str, Any], expected: Dict[str, Any], test_name: str
    ) -> None:
        serialized_output: Optional[str] = lambda_handler(mock, None)
        self.assertTrue(serialized_output, f"{test_name}: None or empty output.")
        deserialized_output: Dict[str, Any] = View.deserialize(serialized_output)
        serialized_mock: str = View.serialize(mock)
        self.assertEqual(
            deserialized_output,
            mock,
            f"{test_name}: Unexpected output: '{deserialized_output}' should be '{mock}'.",
        )
        self.assertEqual(
            serialized_output,
            serialized_mock,
            f"{test_name}: Unexpected output: '{serialized_output}' should be '{serialized_mock}'.",
        )
        print(f"End of test '{test_name}' for test service.")

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
