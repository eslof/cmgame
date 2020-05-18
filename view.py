import json
from json import JSONDecodeError
from enum import Enum

from internal import end
from properties import PacketHeader, ResponseType, ResponseField


class View:
    """todo: look into how base64 would fit in here"""

    encode = json.dumps
    decode = json.loads
    decode_error = JSONDecodeError
    return_type = dict

    @classmethod
    def serialize(cls, data: dict) -> str:
        """Serialize data using current standard format."""
        return cls.encode(data)

    @classmethod
    def try_deserialize(cls, data: str) -> return_type:
        """Try to return deserialized data using current standard format and exit on except."""
        try:
            if not data:
                raise cls.decode_error
            return json.loads(data)
        except cls.decode_error as e:
            end(e.msg)
        return cls.decode(data)

    @classmethod
    def deserialize(cls, data: str) -> return_type:
        """Deserialize data using current standard format."""
        return cls.decode(data)

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
