import json
from properties import PacketHeader, ResponseType, ResponseField


class View:
    @staticmethod
    def _serialize(data: dict) -> str:
        return json.dumps(data)

    @staticmethod
    def construct(response_type: int, data: dict) -> str:
        data[PacketHeader.RESPONSE] = response_type
        return View._serialize(data)

    @staticmethod
    def generic(result: bool) -> str:
        return View._serialize(
            {
                PacketHeader.RESPONSE: ResponseType.GENERIC,
                ResponseField.Generic.RESULT: result,
            }
        )
