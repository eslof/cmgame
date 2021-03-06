import json
from enum import Enum
from functools import partial
from json import JSONDecodeError
from typing import Optional, Any, Dict

from properties import PacketHeader, ResponseType, ResponseField, GameException


class View:
    encode = partial(json.dumps, separators=(",", ":"))
    decode = json.loads
    decode_error = JSONDecodeError

    @classmethod
    def serialize(cls, data: Any) -> str:
        return cls.encode(data)

    @classmethod
    def deserialize(cls, data: str) -> Any:
        return cls.decode(data)  # noqa

    @classmethod
    def response(cls, response_type: Enum, data: Dict[Any, Any]) -> str:
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
    def debug(cls, data: Optional[Any]) -> str:
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
