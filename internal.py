import base64
import json
import secrets
from sys import exit as sys_exit
from typing import Type, Callable

from properties import Constants, PacketHeader
from enum import Enum
from abc import ABC, abstractmethod


class RequestHandler(ABC):
    @staticmethod
    @abstractmethod
    def sanitize(*args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def run(*args, **kwargs):
        pass


def end(message="", code=0) -> None:
    if message:
        # TODO: does logging have a place here? does this method even make sense?
        print(message)
    sys_exit(code)


def generate_id() -> str:
    return base64.b64encode(secrets.token_bytes(Constants.ID_TOKEN_BYTE_COUNT)).decode(
        "ascii"
    )


# TODO: Move some of these hard coded strings somewhere maybe


def sanitize_request(target: dict, request_enum: Type[Enum]) -> None:
    sanitize_field(
        target=target,
        field=PacketHeader.REQUEST,
        sanity=lambda value: isinstance(value, int)
        and value in request_enum._value2member_map_,
        sanity_id=f"Request API ({request_enum})",
    )


def sanitize_field(target: dict, field: str, sanity: Callable, sanity_id: str = "") -> None:
    if not hasattr(target, field) and field not in target:
        end(f"No sane index present ({sanity_id}): {json.dumps(target)}")
    elif not sanity(target[field]):
        end(f"Failed sanity check ({sanity_id}): {field} = {str(target[field])}")


def sanitize_json(target: dict, field: str, sanity_id: str = "") -> None:
    if not hasattr(target, field) and field not in target:
        end(f"No sane index present ({sanity_id}): {json.dumps(target)}")
    elif not isinstance(target[field], str) or not target[field]:
        end(f"Failed sanity check for json contents: {target[field]}")
    else:
        try:
            json.loads(target[field])
        except ValueError as e:
            end(f"Failed sanity check for json: {target[field]} {e}")
