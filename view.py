import json
from properties import PacketHeader, ResponseType, ResponseField


class View:
    @staticmethod
    def serialize(data: dict) -> str:
        """Serialize data using current standard format."""
        return json.dumps(data)

    @staticmethod
    def deserialize(data: str) -> dict:
        """Deserialize data using current standard format."""
        return json.loads(data)

    @staticmethod
    def construct(response_type: int, data: dict) -> str:
        """Create and return a serialized response of given type with given data."""
        data[PacketHeader.RESPONSE] = response_type
        return View.serialize(data)

    @staticmethod
    def generic(result: bool) -> str:
        """Create and return a serialized boolean response as per given result."""
        return View.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.GENERIC,
                ResponseField.Generic.RESULT: result,
            }
        )
