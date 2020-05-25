import secrets
import string
from enum import Enum, EnumMeta
from json import JSONDecodeError
from typing import Callable, Any, Dict

from botocore.exceptions import ClientError  # type: ignore

from database import META_SIZE_LIMIT
from properties import Constants, PacketHeader
from view import View


# TODO: Move some of these hard coded strings somewhere maybe


def end_unless_conditional(e: ClientError) -> None:  # type: ignore
    error = e.response["Error"]["Code"]
    if error != "ConditionalCheckFailedException":
        end(error)  # TODO: error handling
    return


def end(message: str) -> None:
    raise GameException(View.error(message))


class GameException(Exception):
    pass


def generate_id(prefix: str, length: int = Constants.ID_GEN_LENGTH) -> str:
    """TODO: what's good"""
    u_id = "".join(
        secrets.choice(string.ascii_letters + string.digits + "-_")
        for i in range(length)
    )
    return f"{prefix}{u_id}"


def validate_request(target: Dict[str, Any], request_enum: EnumMeta) -> Enum:
    """validate_field wrapper for given enum used for base requests in all lambda_function.py files."""
    validate_field(
        target=target,
        field=PacketHeader.REQUEST,
        validation=lambda value: type(value) is int
        and value in (val.value for val in request_enum.__members__.values()),  # type: ignore
        message=f"Request API ({request_enum.__name__})",
    )
    return request_enum(target[PacketHeader.REQUEST])  # type: ignore


def validate_field(
    target: Dict[str, Any],
    field: str,
    validation: Callable[[Any], bool],
    message: str = "",
) -> None:
    if not hasattr(target, field) and field not in target:
        end(f"No valid attribute present ({message})")
    elif not validation(target[field]):
        end(f"Failed validation ({message}): {field} = {str(target[field])}")


def validate_meta(target: Dict[str, Any], field: str, message: str) -> None:
    max_size = 512 if field not in META_SIZE_LIMIT else META_SIZE_LIMIT[field]
    validate_field(
        target=target,
        field=field,
        validation=lambda value: value and type(value) is str and len(value) < max_size,
        message=message,
    )
    try:
        View.deserialize(target[field])
    except JSONDecodeError as e:
        end(e.msg)
