from default_imports import *
from properties import UserAttr

from .place import Place
from .update import Update

assert_inheritance([Place, Update], RequestHandler)


@unique
class ItemRequest(Enum):
    PLACE = auto()
    UPDATE = auto()


def lambda_handler(event, context):
    """High-level overview: Request is validated, user is authenticated, and
    for each request we .validate the contents and .run the requested action."""

    req = validate_request(event, ItemRequest)
    user_id = User.validate_id(event)

    if req == ItemRequest.PLACE:
        user_data = User.get(
            user_id=user_id,
            attributes=f"{UserAttr.INVENTORY_COUNT}, {UserAttr.CURRENT_HOME}",
        )
        Place.validate(event, user_data)
        result = Place.run(event, user_data)
        return View.generic(result)

    elif req == ItemRequest.UPDATE:
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        Update.validate(event)
        result = Update.run(event, user_data)
        return View.generic(result)
