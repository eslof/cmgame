from unittest import TestCase

from database import UserAttr
from internal import generate_id
from lambda_function import TestRequest
from properties import PacketHeader, RequestField, ResponseField, ResponseType
from view import View
from .test.lambda_function import lambda_handler


class TestService(TestCase):
    mock_id = generate_id(UserAttr.SORT_KEY_PREFIX)

    def run_handler(self, mock_data: dict, expected_output: dict, name: str):
        output: dict = View.deserialize(lambda_handler(mock_data, None))
        self.assertEqual(
            output,
            expected_output,
            f"{name}: Invalid output: '{output}' should be '{expected_output}'.",
        )

    def test_debug(self):
        mock_data = {
            PacketHeader.REQUEST: TestRequest.ONE.value,
            RequestField.User.ID: self.mock_id,
        }
        expected_output = {
            PacketHeader.RESPONSE: ResponseType.DEBUG.value,
            ResponseField.Generic.DEBUG: mock_data,
        }
        self.run_handler(mock_data, expected_output, "View.debug")

    def test_generic(self):
        mock_data = {
            PacketHeader.REQUEST: TestRequest.TWO.value,
            ResponseField.Generic.RESULT: True,
        }
        expected_output = {
            PacketHeader.RESPONSE: ResponseType.GENERIC.value,
            ResponseField.Generic.RESULT: mock_data[ResponseField.Generic.RESULT],
        }
        self.run_handler(mock_data, expected_output, "View.generic")

    def test_error(self):
        error_message = "hello world"
        mock_data = {
            PacketHeader.REQUEST: TestRequest.THREE.value,
            ResponseField.Generic.ERROR: error_message,
        }
        expected_output = {
            PacketHeader.RESPONSE: ResponseType.ERROR.value,
            ResponseField.Generic.ERROR: mock_data[ResponseField.Generic.ERROR],
        }
        self.run_handler(mock_data, expected_output, "View.error")
