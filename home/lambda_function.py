from default_imports import *
from properties import HomeAttr

from .delete import Delete
from .go import Go
from .new import New
from .save import Save

assert_inheritance([Delete, Go, New, Save], RequestHandler)


@unique
class HomeRequest(Enum):
    DELETE = auto()
    GO = auto()
    NEW = auto()
    SAVE = auto()


routes = {
    HomeRequest.DELETE: Route(Delete, View.generic),
    HomeRequest.GO: Route(
        handler=Go,
        output=lambda value: View.construct(
            response_type=ResponseType.HOME_DATA,
            data={
                ResponseField.Home.GRID: value[HomeAttr.GRID],
                ResponseField.Home.META: value[HomeAttr.META],
            },
        ),
    ),
    HomeRequest.NEW: Route(New, View.generic),
    HomeRequest.SAVE: Route(Save, View.generic),
}


def lambda_handler(event, context):
    """Return of 'handler.validate()' is passed to 'handler.run()'.
    Finally the return value of 'handler.run()' is passed to associated 'route.output()'."""

    user_id = User.validate_id(event)
    req = validate_request(event, HomeRequest)

    with routes[req] as route:
        handler = route.handler
        output = route.output

    valid_data = handler.validate(event, user_id)
    output(handler.run(event, user_id, valid_data))
