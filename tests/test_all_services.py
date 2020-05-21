import importlib
import os
from enum import Enum, EnumMeta
from inspect import isclass
from typing import Callable
from unittest import TestCase

import router
from database import UserAttr
from internal import generate_id
from properties import RequestField, Constants, PacketHeader
from request_handler import RequestHandler


# todo: update for enum meta
class TestService(TestCase):

    LAMBDA_HANDLER_NAME = "lambda_handler"
    LAMBDA_FILE_NAME = "lambda_function"
    ROOT_DIR = ".."
    MOCK_USER_PACKET = {
        PacketHeader.REQUEST: 1,
        RequestField.User.ID: generate_id(UserAttr.SORT_KEY_PREFIX),
    }

    def test_all_services(self):
        dir_list = [
            name
            for name in os.listdir(self.ROOT_DIR)
            if os.path.isdir(os.path.join(self.ROOT_DIR, name))
        ]
        for directory in dir_list:
            for name in os.listdir(f"{self.ROOT_DIR}/{directory}"):
                if name == f"{self.LAMBDA_FILE_NAME}.py":
                    service = importlib.import_module(
                        f"{directory}.{self.LAMBDA_FILE_NAME}"
                    )
                    func = getattr(service, self.LAMBDA_HANDLER_NAME)
                    with self.subTest(directory):
                        self.lambda_handler_subTest(func, directory)

    def lambda_handler_subTest(self, lambda_handler: Callable, name: str):
        def test_handler(handler: type):
            # region Assert that our handler base class is not broken
            self.assertTrue(
                RequestHandler and isclass(RequestHandler),
                f"{name}: Broken or missing RequestHandler base: '{RequestHandler}'.",
            )
            # endregion

            # region Assert that the given handler for this route is valid
            self.assertTrue(handler, f"{name}: Invalid handler: '{handler}'")
            # TODO: check if we can trick this by deriving
            self.assertTrue(
                isclass(type(handler)),
                f"{name}: Invalid handler: '{handler}' not instance of class.",
            )
            self.assertTrue(
                issubclass(handler, RequestHandler)
                and not (handler is RequestHandler)
                and not (type(handler) is RequestHandler),
                f"{name}: Invalid inheritance: '{handler}' not derive '{RequestHandler}'.",
            )
            # endregion

        def test_route(routes, enum):
            # region Assert that the given route is valid
            self.assertTrue(
                routes[enum],
                f"{name}: Invalid route: '{routes[enum]}' in '{routes}' at '{enum}'.",
            )
            self.assertTrue(
                isinstance(routes[enum], router.Route),
                f"{name}: Invalid route: '{routes[enum]}' not instance of '{router.Route}' in '{routes}' at '{enum}'.",
            )
            # endregion

            # region Assert that the route's handler and output are valid
            test_handler(routes[enum].handler)
            self.assertTrue(
                routes[enum].output,
                f"{name}: Invalid output: '{routes[enum].output}' for '{routes[enum]}' in '{routes}' at '{enum}'.",
            )
            self.assertTrue(
                callable(routes[enum].output),
                f"{name}: Invalid output: '{routes[enum].output}' not callable for '{routes[enum]}' in '{routes}' at '{enum}'.",
            )
            #   endregion

        def test_wrapper(routes: dict, request_enum: EnumMeta, f, *args):
            # region Assert decorated function to be 'lambda_handler' with at least one argument
            self.assertTrue(
                len(args) > 0 and args[0] and type(args[0]) is dict,
                f"{name}: Incorrect first argument for '{Constants.LAMBDA_HANDLER_NAME}' in '{request_enum}', should be '{Constants.LAMBDA_HANDLER_NAME}(event, context)'.",
            )
            self.assertTrue(
                f.__name__ == self.LAMBDA_HANDLER_NAME,
                f"{name}: Invalid function: '{f.__name__}' for '{request_enum}', should be '{self.LAMBDA_HANDLER_NAME}'.",
            )
            # endregion

            # region Assert rout dict and request enum
            self.assertTrue(
                routes and type(routes) is dict,
                f"{name}: Invalid routes dict: '{routes}'.",
            )
            self.assertTrue(
                request_enum
                and isclass(request_enum)
                and issubclass(request_enum, Enum)
                and len(request_enum),
                f"{name}: Invalid request_enum: '{request_enum}'",
            )
            # endregion

            # region Assert that all entries in routes dict are valid
            for enum in routes:
                self.assertTrue(
                    issubclass(type(enum), Enum),
                    f"{name}: Invalid key type: {type(enum)}",
                )
                self.assertTrue(
                    type(enum) is request_enum,
                    f"{name}: Invalid entry '{enum}' in '{routes}'.",
                )
                self.assertTrue(
                    enum in request_enum,
                    f"{name}: Invalid entry: '{enum}' not in '{request_enum}'.",
                )
                test_route(routes, enum)
            # endregion

            # region Assert that all members of request enum are present
            for enum in request_enum:
                self.assertTrue(
                    enum in routes, f"{name}: Invalid entry: '{enum}' not in '{routes}"
                )
                test_route(routes, enum)
            # endregion

        router.wrapper = test_wrapper
        event = self.MOCK_USER_PACKET
        lambda_handler(event, None)
