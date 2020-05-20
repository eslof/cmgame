import unittest
from enum import IntEnum
from inspect import isclass
from typing import Type
from unittest.mock import patch, Mock
import router
import friend.lambda_function
from properties import Constants, RequestField
from request_handler import RequestHandler

LAMBDA_HANDLER_NAME = "lambda_handler"


class Test(unittest.TestCase):
    def test_routing(self):
        def test_handler(handler: type):
            # region Assert that our handler base class is not broken
            self.assertTrue(
                RequestHandler and isclass(RequestHandler),
                f"Broken or missing RequestHandler base: '{RequestHandler}'.",
            )
            # endregion

            # region Assert that the given handler for this route is valid
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
            # endregion

        def test_route(routes, enum):
            # region Assert that the given route is valid
            self.assertTrue(
                routes[enum],
                f"Invalid route: '{routes[enum]}' in '{routes}' at '{enum}'.",
            )
            self.assertTrue(
                isinstance(routes[enum], router.Route),
                f"Invalid route: '{routes[enum]}' not instance of '{router.Route}' in '{routes}' at '{enum}'.",
            )
            # endregion

            # region Assert that the route's handler and output are valid
            test_handler(routes[enum].handler)
            self.assertTrue(
                routes[enum].output,
                f"Invalid output: '{routes[enum].output}' for '{routes[enum]}' in '{routes}' at '{enum}'.",
            )
            self.assertTrue(
                callable(routes[enum].output),
                f"Invalid output: '{routes[enum].output}' not callable for '{routes[enum]}' in '{routes}' at '{enum}'.",
            )
            #   endregion

        def test_wrapper(routes: dict, request_enum: type(IntEnum), f, *args):
            # region Assert decorated function to be 'lambda_handler' with at least one argument
            self.assertTrue(
                len(args) > 0 and args[0] and type(args[0]) is dict,
                f"Incorrect first argument for '{Constants.LAMBDA_HANDLER_NAME}' in '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}(event, context)'.",
            )
            self.assertTrue(
                f.__wrapped__ == LAMBDA_HANDLER_NAME,
                f"Invalid function: '{f.__name__}' for '{request_enum}', should be '{LAMBDA_HANDLER_NAME}'.",
            )
            # endregion

            # region Assert rout dict and request enum
            self.assertTrue(
                routes and type(routes) is dict, f"Invalid routes dict: '{routes}'."
            )
            self.assertTrue(
                request_enum
                and isclass(request_enum)
                and issubclass(request_enum, IntEnum)
                and len(request_enum),
                f"Invalid request_enum: '{request_enum}'",
            )
            # endregion

            # region Assert that all entries in routes dict are valid
            for enum in routes:
                self.assertTrue(
                    enum in request_enum,
                    f"Invalid entry: '{enum}' not in '{request_enum}'.",
                )
                test_route(routes, enum)
            # endregion

            # region Assert that all members of request enum are present
            for enum in request_enum:
                self.assertTrue(
                    enum in routes, f"Invalid entry: '{enum}' not in '{routes}"
                )
                test_route(routes, enum)
            # endregion

        with patch("router.wrapper", side_effect=test_wrapper):
            lambda_function = friend.lambda_function.lambda_handler
            event = {RequestField.User.ID: "UyBYaH9ItbEmv6aOjRnCeV"}
            lambda_function(event, None)
