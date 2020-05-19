import string
import secrets
from enum import Enum
from inspect import isclass
from properties import Constants, PacketHeader
from sys import exit as sys_exit
from typing import Callable, Union, List, Any


# TODO: Move some of these hard coded strings somewhere maybe


def end_unless_conditional(e):
    error = e.response["Error"]["Code"]
    if e.response["Error"]["Code"] != "ConditionalCheckFailedException":
        end(error)  # TODO: error handling


def assert_inheritance(target: Union[type, List[type]], base: type):
    """Assert that given class, or list of classes, inherit from given base class.
    todo: current implementation of these I guess could be moved to unit testing"""
    if not isclass(base):
        end(f"Failed assert_inheritance: {base} is not a class type (base).")
    if type(target) is list:
        for obj in target:
            if not isclass(type(obj)):
                end(f"Failed assert_inheritance: {obj} is not an instance of a class.")
            elif not issubclass(obj, base) or obj is base or type(target) is base:
                end(f"Failed assert_inheritance: {obj} does not inherit from {base}.")
    elif not isclass(type(target)):
        end(f"Failed assert_inheritance: {target} is not an instance of a class.")
    elif not issubclass(target, base) or target is base or type(target) is base:
        end(f"Failed assert_inheritance: {target} does not inherit from {base}.")


def end(message: str = "", code: int = 0) -> None:
    """Wrapper for exit at case outcomes that are not expected by client without possible misuse or corruption."""
    if message:
        pass
        # View.error(message)
    sys_exit(code)


def generate_id(prefix: str, length: int = Constants.ID_GEN_LENGTH) -> str:
    """TODO: what's good"""
    return prefix + (
        "".join(
            secrets.choice(string.ascii_letters + string.digits + "-_")
            for i in range(length - 1)
        )
    )


def validate_request(
    target: dict, request_enum: type(Enum), field: str = PacketHeader.REQUEST
) -> Enum:
    """validate_field wrapper for given enum used for base requests in all lambda_function.py files."""
    validate_field(
        target=target,
        field=field,
        validation=lambda value: type(value) is int
        and value in request_enum._value2member_map_,
        message=f"Request API ({request_enum.__name__})",
    )
    return request_enum(target[field])


def validate_field(
    target: dict, field: str, validation: Callable[[Any], bool], message: str = ""
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
        validation=lambda value: value and type(value) is str,
        message=message,
    )
    try:
        # View.deserialize(target[field])
        hi = 1 + 2
    except ValueError as e:
        end(f"Failed validation of meta during decoding: {target[field]} {e}")
