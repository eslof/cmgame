import json
from enum import Enum
from typing import Type

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
    def construct(response_type: Enum, data: dict) -> str:
        """Create and return a .serialize'd response of given type with given data."""
        data[PacketHeader.RESPONSE] = response_type.value
        return View.serialize(data)

    @staticmethod
    def generic(result: bool) -> str:
        """Create and return a .serialize'd boolean response as per given result."""
        return View.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.GENERIC.value,
                ResponseField.Generic.RESULT: result,
            }
        )
