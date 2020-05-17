from default_imports import *

from .place import Place
from .update import Update

assert_inheritance([Place, Update], RequestHandler)


@unique
class ItemRequest(Enum):
    PLACE = auto()
    UPDATE = auto()


routes = {
    ItemRequest.PLACE: Route(Place, View.generic),
    ItemRequest.UPDATE: Route(Update, View.generic),
}


def lambda_handler(event, context):
    """Return of 'handler.validate()' is passed to 'handler.run()'.
    Finally the return value of 'handler.run()' is passed to associated 'route.output()'."""

    user_id = User.validate_id(event)
    req = validate_request(event, ItemRequest)

    with routes[req] as route:
        handler = route.handler
        output = route.output

    valid_data = handler.validate(event, user_id)
    output(handler.run(event, user_id, valid_data))
