from default_imports import *

from .accept import Accept
from .demand import Demand

assert_inheritance([Accept, Demand], RequestHandler)


@unique
class ItemBoxRequest(Enum):
    ACCEPT = auto()
    DEMAND = auto()


routes = {
    ItemBoxRequest.ACCEPT: Route(Accept, View.generic),
    ItemBoxRequest.DEMAND: Route(Demand, View.generic),
}


def lambda_handler(event, context):
    """Return of 'handler.validate()' is passed to 'handler.run()'.
    Finally the return value of 'handler.run()' is passed to associated 'route.output()'."""

    user_id = User.validate_id(event)
    req = validate_request(event, ItemBoxRequest)

    with routes[req] as route:
        handler = route.handler
        output = route.output

    valid_data = handler.validate(event, user_id)
    output(handler.run(event, user_id, valid_data))
