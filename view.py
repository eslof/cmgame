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
        return cls.encode(data)

    @classmethod
    def deserialize(cls, data: str) -> Dict[str, Any]:
        return cls.decode(data)  # type: Dict[str, Any]

    @classmethod
    def response(cls, response_type: Enum, data: Dict[str, Any]) -> str:
        data[PacketHeader.RESPONSE] = response_type
        return cls.serialize(data)

    @classmethod
    def generic(cls, result: bool) -> str:
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
        return cls.serialize(
            {
                PacketHeader.RESPONSE: ResponseType.ERROR.value,
                ResponseField.Generic.Error.TYPE: error_type,
                ResponseField.Generic.Error.MESSAGE: message,
            }
        )
