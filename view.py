import json
from enum import Enum

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

    @classmethod
    def response(cls, response_type: Enum, data: dict) -> str:
        """Create and return a .serialize'd response of given type with given data."""
        data[PacketHeader.RESPONSE] = response_type.value
        return cls.serialize(data)

    @classmethod
    def generic(cls, result: bool) -> str:
        """Create and return a .serialize'd boolean response as per given result."""
        return cls.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.GENERIC.value,
                ResponseField.Generic.RESULT: result,
            }
        )

    @classmethod
    def error(cls, message: str) -> str:
        """Create and return a .serialize'd error response with given message."""
        return cls.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.ERROR.value,
                ResponseField.Generic.ERROR: message,
            }
        )
