import json
from enum import Enum
from json import JSONDecodeError
from typing import Optional, Any, Dict

from properties import PacketHeader, ResponseType, ResponseField, GameException


class View:
    encode = lambda value: json.dumps(value, separators=(",", ":"))
    decode = json.loads
    decode_error = JSONDecodeError

    @classmethod
    def serialize(cls, data: Any) -> str:
        """Serialize data using current standard format."""
        return cls.encode(data)

    @classmethod
    def deserialize(cls, data: str) -> Dict[str, Any]:
        """Deserialize data using current standard format."""
        return cls.decode(data)  # type: Dict[str, Any]

    @classmethod
    def response(cls, response_type: Enum, data: Dict[str, Any]) -> str:
        """Create and return a .serialize'd response of given type with given data."""
        data[PacketHeader.RESPONSE] = response_type
        return cls.serialize(data)

    @classmethod
    def generic(cls, result: bool) -> str:
        """Create and return a .serialize'd boolean response as per given result."""
        return cls.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.GENERIC.value,
                ResponseField.Generic.RESULTS: result,
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
    def error(cls, message: str, error_type: str = GameException.__name__) -> str:
        """Create and return a .serialize'd error response with given message."""
        return cls.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.ERROR.value,
                ResponseField.Generic.ERROR_TYPE: error_type,
                ResponseField.Generic.ERROR_MESSAGE: message,
            }
        )
