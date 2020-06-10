import random
from enum import EnumMeta, Enum
from typing import Dict, Callable, Any, Union

from botocore.exceptions import ClientError  # noqa

from properties import Constants, PacketHeader, GameException
from view import View


def end(message: str) -> None:
    raise GameException(View.error(message))


def web_socket_endpoint() -> Dict[str, Union[str, int]]:
    #  TODO: get live state
    return {"response_code": 200, "address": "domain.com/ws"}


def generate_id(prefix: str) -> str:
    return "".join(
        [
            prefix,
            "".join(random.choices(Constants.ID_CHARSET, k=Constants.ID_GEN_LENGTH)),
        ]
    )


def validate_request(
    target: Dict[str, Any], request_enum: EnumMeta, field=PacketHeader.REQUEST
) -> Enum:
    validate_field(
        target=target,
        field=field,
        value_type=int,
        validation=lambda v: v
        in (val.value for val in request_enum.__members__.values()),
        message=f"Request API ({request_enum.__name__})",
    )
    return request_enum(target[PacketHeader.REQUEST])


def validate_field(
    target: Dict[str, Any],
    field: str,
    value_type: type,
    validation: Callable[[Any], Any],
    message: str,
) -> None:
    if not hasattr(target, field) and field not in target:
        end(f"No valid attribute present ({message}): {field} not in {target}.")
    if not type(target[field]) is value_type:
        end(f"Value type error ({message}): {target[field]} != {value_type}.")
    elif not validation(target[field]):
        end(f"Failed validation ({message}): {field} = {target[field]}.")


def validate_choice(target: Dict[str, Any], field: str, max: int, message: str) -> None:
    validate_field(target, field, int, lambda v: 0 < v <= max, message)


def validate_name(
    target: Dict[str, Any], field: str, max_length: int, message: str
) -> None:
    validate_field(target, field, str, lambda v: 0 < len(v) <= max_length, message)


def validate_meta(
    target: Dict[str, Any], field: str, max_size: int, message: str
) -> None:
    validate_field(
        target, field, str, lambda v: v and len(v) < max_size, message,
    )
    try:
        View.deserialize(target[field])
    except View.decode_error as e:
        end(e.msg)
