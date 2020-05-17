#set($sc = ${service})
#set($r1c = ${StringUtils.removeUnderScores(${request_1})})
#set($r1l = $request_1.toLowerCase())
#set($r1u = $request_1.toUpperCase())
#set($r2c = ${StringUtils.removeUnderScores(${request_2})})
#set($r2l = $request_2.toLowerCase())
#set($r2u = $request_2.toUpperCase())
from default_imports import *

from .${r1l} import ${r1c}
from .${r2l} import ${r2c}

assert_inheritance([${r1c}, ${r2c}], RequestHandler)


@unique
class ${sc}Request(Enum):
    ${r1u} = auto()
    ${r2u} = auto()


routes = {
    ${sc}Request.$r1u: Route(${r1c}, View.generic),
    ${sc}Request.$r2u: Route(${r2c}, View.generic)
}


def lambda_handler(event, context):
    """Return of 'handler.validate()' is passed to 'handler.run()'.
    Finally the return value of 'handler.run()' is passed to associated 'route.output()'."""

    user_id = User.validate_id(event)
    req = validate_request(event, ${sc}Request)

    with routes[req] as route:
        handler = route.handler
        output = route.output

    valid_data = handler.validate(event, user_id)
    output(handler.run(event, user_id, valid_data))
