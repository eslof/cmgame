from abc import ABC, abstractmethod
from base64 import b64encode
from enum import Enum
from inspect import isclass
from secrets import token_bytes
from sys import exit as sys_exit
from typing import Callable, Union, List, Type

from properties import Constants, PacketHeader
from view import View


# TODO: Move some of these hard coded strings somewhere maybe


def assert_inheritance(target: Union[type, List[type]], base: type):
    """Assert that given class, or list of classes, inherit from given base class."""
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


# TODO: metaclass=abc.ABCMeta ? research
class RequestHandler(ABC):
    """Modules used by our AWS Lambda functions inherit this ABC.
    This to help maintain the architecture of the application.
    Refer to RequestHandlerTemplate.py"""

    @staticmethod
    @abstractmethod
    def validate(*args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def run(*args, **kwargs):
        pass


def end(message: str = "", code: int = 0) -> None:
    """Wrapper for exit at case outcomes that are not expected by client without possible misuse or corruption."""
    if message:
        # TODO: does logging have a place here? does this method even make sense?
        print(View.serialize({"debug": message}))
    sys_exit(code)


def generate_id() -> str:
    """TODO: what's good"""
    return b64encode(token_bytes(Constants.ID_TOKEN_BYTE_COUNT)).decode("ascii")


def validate_request(
    target: dict, request_enum: Type[Enum], field: str = PacketHeader.REQUEST
) -> Enum:
    """validate_field wrapper for given enum used for base requests in all lambda_function.py files."""
    validate_field(
        target=target,
        field=field,
        validation=lambda value: isinstance(value, int)
        and value in request_enum._value2member_map_,
        message=f"Request API ({request_enum.__name__})",
    )
    return request_enum(target[field])


def validate_field(
    target: dict, field: str, validation: Callable, message: str = ""
) -> None:
    """Confirm that the given field exists in target and perform given validation on its content."""
    if not hasattr(target, field) and field not in target:
        end(f"No valid attribute present ({message}): {View.serialize(target)}")
    elif not validation(target[field]):
        end(f"Failed validation ({message}): {field} = {str(target[field])}")


def validate_meta(target: dict, field: str, message: str = "") -> None:
    """validate_field and confirm that contents follow the correct format."""
    validate_field(
        target=target,
        field=field,
        validation=lambda value: isinstance(value, str) and value,
        message=message,
    )
    try:
        View.deserialize(target[field])
    except ValueError as e:
        end(f"Failed validation of meta during decoding: {target[field]} {e}")
