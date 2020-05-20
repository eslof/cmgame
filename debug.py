if __debug__:
    from enum import Enum
    from inspect import isclass
    from request_handler import RequestHandler

    LAMBDA_HANDLER_NAME = "lambda_handler"

    def assert_handler(handler: type):
        assert RequestHandler and isclass(
            RequestHandler
        ), f"Broken or missing RequestHandler base: '{RequestHandler}'."
        assert handler, f"Invalid handler: '{handler}'"
        # TODO: check if we can trick this by deriving
        assert isclass(
            type(handler)
        ), f"Invalid handler: '{handler}' not instance of class."
        assert (
            issubclass(handler, RequestHandler)
            and not (handler is RequestHandler)
            and not (type(handler) is RequestHandler)
        ), f"Invalid inheritance: '{handler}' not derive '{RequestHandler}'."

    def assert_route(routes: dict, enum: Enum, route_class: type):
        assert routes[
            enum
        ], f"Invalid route: '{routes[enum]}' in '{routes}' at '{enum}'."
        assert isinstance(
            routes[enum], route_class
        ), f"Invalid route: '{routes[enum]}' not instance of '{route_class}' in '{routes}' at '{enum}'."
        assert_handler(routes[enum].handler)
        assert routes[
            enum
        ].output, f"Invalid output: '{routes[enum].output}' for '{routes[enum]}' in '{routes}' at '{enum}'."
        assert callable(
            routes[enum].output
        ), f"Invalid output: '{routes[enum].output}' not callable for '{routes[enum]}' in '{routes}' at '{enum}'."

    # todo: move to unit test (?)
    def assert_routing(
        f_name: str, routes: dict, request_enum: type(Enum), route_class: type
    ):
        assert isclass(
            route_class
        ), f"Invalid route class: {route_class} should be class."
        assert (
            f_name == LAMBDA_HANDLER_NAME
        ), f"Invalid function: '{f_name}' for '{request_enum}', should be '{LAMBDA_HANDLER_NAME}'."
        assert routes and type(routes) is dict, f"Invalid routes dict: '{routes}'."
        assert (
            request_enum and isclass(request_enum) and len(request_enum)
        ), f"Invalid request_enum: '{request_enum}'"
        for enum in routes:
            assert (
                enum in request_enum
            ), f"Invalid entry: '{enum}' not in '{request_enum}'."
            assert_route(routes, enum, route_class)
        for enum in request_enum:
            assert enum in routes, f"Invalid entry: '{enum}' not in '{routes}"
            assert_route(routes, enum, route_class)
