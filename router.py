from typing import Type, Callable, Any, Optional
from internal import validate_request
from request_handler import RequestHandler
from user import User
from enum import Enum


class Route(object):
    def __init__(self, handler: Type[RequestHandler], output: Callable):
        self.handler = handler
        self.output = output


def lambda_handler(event: dict, context: Optional[Any], router: Route):
    user_id = User.validate_id(event)
    valid_data = router.handler.validate(event, user_id)
    output = router.handler.run(event, user_id, valid_data)
    router.output(output)


def route(routers: dict, request_enum: Type[Enum]):
    def inner(f):
        def wrapped_f(*args):
            req = validate_request(args[0], request_enum)
            args = args + (routers[req])
            return lambda_handler(*args)

        return wrapped_f

    return inner
