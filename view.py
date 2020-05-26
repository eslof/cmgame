import json
from enum import Enum
from json import JSONDecodeError
from typing import Optional, Any, Tuple, Dict

from properties import PacketHeader, ResponseType, ResponseField


class View:
    # todo: look into how a different serialization lib would fit here
    # todo: look into typing

    encode = json.dumps
    decode = json.loads
    decode_error = JSONDecodeError
    valid_empty = "{}"
    separators: Tuple[str, str] = ",", ":"

    @classmethod
    def serialize(cls, data: dict) -> str:
        """Serialize data using current standard format."""
        return cls.encode(data, separators=cls.separators)

    @classmethod
    def deserialize(cls, data: Optional[str]) -> Dict[str, Any]:
        """Deserialize data using current standard format."""
        return cls.decode(data)

    @classmethod
    def response(cls, response_type: Enum, data: dict) -> str:
        """Create and return a .serialize'd response of given type with given data."""
        data[PacketHeader.RESPONSE] = response_type
        return cls.serialize(data)

    @classmethod
    def generic(cls, result: Optional[bool]) -> str:
        """Create and return a .serialize'd boolean response as per given result."""
        return cls.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.GENERIC.value,
                ResponseField.Generic.RESULT: False if result is None else result,
            }
        )

    @classmethod
    def debug(cls, data: Optional[Any]):
        return cls.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.DEBUG.value,
                ResponseField.Generic.DEBUG: data,
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
