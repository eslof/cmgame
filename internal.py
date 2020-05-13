import base64
import json
import secrets
from inspect import isclass
from sys import exit as sys_exit
from typing import Type, Callable, Union, List

from properties import Constants, PacketHeader
from enum import Enum
from abc import ABC, abstractmethod


# TODO: Move some of these hard coded strings somewhere maybe

def assert_inheritance(target: Union[type, List[type]], base: type):
    if isinstance(target, list):
        for obj in target:
            if not isclass(obj):
                end(f"Misuse of assert_inheritance (Not a class)")
            elif not issubclass(obj, base):
                end(f"Architecture broken ({target} != {base})")
    elif not isclass(target):
        end(f"Misuse of assert_inheritance (Not a class)")
    elif not issubclass(target, base):
        end(f"Architecture broken ({target} != {base})")


class RequestHandler(ABC):
    @staticmethod
    @abstractmethod
    def validate(*args, **kwargs):
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


def validate_request(target: dict, request_enum: Type[Enum]) -> None:
    validate_field(
        target=target,
        field=PacketHeader.REQUEST,
        validation=lambda value: isinstance(value, int)
        and value in request_enum._value2member_map_,
        validation_id=f"Request API ({request_enum.__name__})",
    )


def validate_field(target: dict, field: str, validation: Callable, validation_id: str = "") -> None:
    if not hasattr(target, field) and field not in target:
        end(f"No valid index present ({validation_id}): {json.dumps(target)}")
    elif not validation(target[field]):
        end(f"Failed validation ({validation_id}): {field} = {str(target[field])}")


def validate_meta(target: dict, field: str, validation_id: str = "") -> None:
    if not hasattr(target, field) and field not in target:
        end(f"No valid index present ({validation_id}): {json.dumps(target)}")
    elif not isinstance(target[field], str) or not target[field]:
        end(f"Content not present or wrong type: {target[field]}")
    else:
        try:
            # TODO: View._decode
            json.loads(target[field])
        except ValueError as e:
            end(f"Failed validation of meta during decoding: {target[field]} {e}")
