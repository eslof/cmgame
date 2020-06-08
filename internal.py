import random
from enum import EnumMeta, Enum
from typing import Dict, Callable, Any, Union

from botocore.exceptions import ClientError  # noqa

from config import Config
from properties import Constants, PacketHeader, GameException
from view import View


def end_unless_conditional(e: ClientError) -> None:
    error = e.response["Error"]["Code"]
    if error != "ConditionalCheckFailedException":
        end(error)  # TODO: error handling
    return


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


def validate_request(target: Dict[str, Any], request_enum: EnumMeta) -> Enum:
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


def validate_meta(
    target: Dict[str, Any], field: str, max_size: int, message: str
) -> None:
    validate_field(
        target=target,
        field=field,
        validation=lambda value: value and type(value) is str and len(value) < max_size,
        message=message,
    )
    try:
        View.deserialize(target[field])
    except View.decode_error as e:
        end(e.msg)
