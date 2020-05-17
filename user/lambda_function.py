from default_imports import *

from .data import Data
from .delete import Delete
from .new import New
from .save import Save

assert_inheritance([Data, Delete, New, Save], RequestHandler)


@unique
class UserRequest(Enum):
    NEW = auto()
    DATA = auto()
    SAVE = auto()
    DELETE = auto()


def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    req = validate_request(target=event, request_enum=UserRequest)

    if req == UserRequest.NEW:
        New.validate(event)
        encrypted_uuid = New.run(event)
        return View.construct(
            response_type=ResponseType.WELCOME,
            data={ResponseField.User.ID: encrypted_uuid},
        )

    user_id = User.validate_id(event)

    if req == UserRequest.DATA:
        user_data = Data.run(user_id)
        return View.construct(
            response_type=ResponseType.WELCOME,
            data={ResponseField.User.DATA: user_data},
        )

    elif req == UserRequest.SAVE:
        Save.validate(event)
        result = Save.run(event, user_id)
        return View.generic(result)

    elif req == UserRequest.DELETE:
        Delete.validate(event)
        result = Delete.run(user_id)
        return View.generic(result)
