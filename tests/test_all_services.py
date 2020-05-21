import importlib
import os
from enum import Enum, EnumMeta
from inspect import isclass
from typing import Callable, Any, Dict, Type, Optional
from unittest import TestCase
from unittest.mock import patch
from collections.abc import Sized
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

    def test_all_services(self) -> None:
        dir_list = [
            name
            for name in os.listdir(self.ROOT_DIR)
            if os.path.isdir(os.path.join(self.ROOT_DIR, name))
        ]
        for directory in dir_list:
            for name in os.listdir(f"{self.ROOT_DIR}/{directory}"):

                # region For each submodule with a lambda_function
                if name == f"{self.LAMBDA_FILE_NAME}.py":
                    service = importlib.import_module(
                        f"{directory}.{self.LAMBDA_FILE_NAME}"
                    )
                    func = getattr(service, self.LAMBDA_HANDLER_NAME)
                    with self.subTest(directory):
                        self.lambda_handler_subTest(func, directory)
                # endregion

    def lambda_handler_subTest(
        self, lambda_handler: Callable[[Dict[str, Any], Any], None], name: str
    ) -> None:
        def test_handler(handler: Type[RequestHandler]) -> None:
            # region Assert that our handler base class is not broken
            self.assertTrue(
                RequestHandler and isclass(RequestHandler),
                f"{name}: Broken or missing RequestHandler base: '{RequestHandler}'.",
            )
            # endregion

            # region Assert that the given handler for this route is valid
            self.assertTrue(
                handler
                and isclass(handler)
                and issubclass(handler, RequestHandler)
                and not (handler is RequestHandler),
                f"{name}: Invalid inheritance: '{handler}' must derive '{RequestHandler}'.",
            )
            # endregion

        def test_route(routes: router.ROUTES_TYPE, enum: Enum) -> None:
            # region Assert that the given route is valid
            self.assertTrue(
                routes[enum]
                and isinstance(routes[enum], router.Route)
                and not (routes[enum] is router.Route),
                f"{name}: Invalid route: '{routes[enum]}' not instance of '{router.Route}' in '{routes}' at '{enum}'.",
            )
            # endregion

            # region Assert that the route's handler and output are valid
            test_handler(routes[enum].handler)
            self.assertTrue(
                routes[enum].output and callable(routes[enum].output),
                f"{name}: Invalid output function: '{routes[enum].output}' for '{routes[enum]}' in '{routes}' at '{enum}'.",
            )
            #   endregion

        def test_wrapper(
            routes: router.ROUTES_TYPE,
            request_enum: EnumMeta,
            f: Callable[[Dict[str, Any], Dict[str, Any]], None],
            event: Dict[str, Any],
        ) -> str:
            # region Assert decorated function to be 'lambda_handler' with at least one argument
            self.assertTrue(
                event and type(event) is dict,
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
                and isinstance(request_enum, EnumMeta)
                and isinstance(request_enum, Sized)
                and len(request_enum),
                f"{name}: Invalid request enum: '{request_enum}'.",
            )
            # endregion

            # region Assert that all entries in routes dict are valid
            for key in routes:
                self.assertTrue(
                    isinstance(key, Enum)
                    and type(key) is request_enum
                    and key in request_enum,
                    f"{name}: Invalid entry '{key}' in '{routes}' not associated with '{request_enum}'.",
                )
                test_route(routes, key)
            # endregion

            # region Assert that all members of request enum have a route
            for key in request_enum:
                self.assertTrue(
                    key in routes, f"{name}: Missing route: '{key}' not in '{routes}'."
                )
                test_route(routes, key)
            # endregion
            return ""

        with patch.object(router, "wrapper", new=test_wrapper):
            # router.wrapper = test_wrapper
            event = self.MOCK_USER_PACKET
            lambda_handler(event, None)
