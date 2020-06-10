import importlib
import os
import sys
from enum import Enum, EnumMeta
from inspect import isclass
from types import ModuleType
from typing import Callable, Any, Dict, Type
from unittest import TestCase
from unittest.mock import patch

import router
from db_properties import UserAttr
from internal import generate_id
from properties import RequestField, PacketHeader
from request_handler import RequestHandler


# **FOLD ALL REGIONS** until TODO: make this more manageable


class TestAllServices(TestCase):

    # region Const members
    def setUp(self) -> None:
        self.LAMBDA_HANDLER_NAME = "lambda_handler"
        self.LAMBDA_FILE_NAME = "lambda_function"
        self.ROOT_DIR = ".."
        self.MOCK_USER_PACKET = {
            PacketHeader.REQUEST: 1,
            RequestField.User.ID: generate_id(UserAttr.SORT_KEY_PREFIX),
        }

    # endregion

    def test_all_services(self) -> None:
        dir_list = [
            name
            for name in os.listdir(self.ROOT_DIR)
            if os.path.isdir(os.path.join(self.ROOT_DIR, name))
        ]
        for directory in dir_list:
            for name in os.listdir(f"{self.ROOT_DIR}/{directory}"):
                if name == f"{self.LAMBDA_FILE_NAME}.py":
                    # region SubTest for each folder in root with lambda_function
                    with self.subTest(directory):
                        # region Assert lambda_handler exists and is decorated
                        module_path = f"../{directory}"
                        if module_path not in sys.path:
                            sys.path.append(f"../{directory}")
                        service = importlib.import_module(f"{self.LAMBDA_FILE_NAME}")
                        sys.path.remove(module_path)
                        self.assertTrue(
                            hasattr(service, self.LAMBDA_HANDLER_NAME),
                            f"{directory}: Missing '{self.LAMBDA_HANDLER_NAME}'"
                            f" in module '{self.LAMBDA_FILE_NAME}'",
                        )
                        func = getattr(service, self.LAMBDA_HANDLER_NAME)
                        self.assertTrue(
                            func
                            and hasattr(func, "__decorated__")
                            and func.__decorated__
                            and func.__decorated__ == "route",
                            f"{directory}: Undecorated '{self.LAMBDA_HANDLER_NAME}'"
                            f" in module '{self.LAMBDA_FILE_NAME}'",
                        )
                        # endregion
                        self.lambda_handler_subTest(func, directory)
                    # endregion
        print("End of implementation test for all services.")

    def lambda_handler_subTest(
        self, lambda_handler: router.LambdaHandler, name: str,
    ) -> None:
        def test_handler(handler: Type[RequestHandler]) -> None:
            # region Assert that our handler base class is not broken
            # TODO: this kinda feels unnecessary
            self.assertTrue(
                RequestHandler and isclass(RequestHandler),
                f"{name}: Broken or missing RequestHandler base:"
                f" '{RequestHandler}'.",
            )
            # endregion

            # region Assert that the given handler for this route is valid
            self.assertTrue(
                handler
                and isclass(handler)
                and issubclass(handler, RequestHandler)
                and not (handler is RequestHandler),
                f"{name}: Invalid inheritance: '{handler}'"
                f" must derive '{RequestHandler}'.",
            )
            # endregion

        def test_route(routes: router.ROUTES_TYPE, enum: Enum) -> None:
            # region Assert that the given route is valid
            self.assertTrue(
                routes[enum]
                and isinstance(routes[enum], router.Route)
                and not (routes[enum] is router.Route),
                f"{name}: Invalid route: '{routes[enum]}' not instance of"
                f" '{router.Route}' in '{routes}' at '{enum}'.",
            )
            # endregion

            # region Assert that the route's handler and output are valid
            test_handler(routes[enum].handler)
            self.assertTrue(
                routes[enum].output and callable(routes[enum].output),
                f"{name}: Invalid output function: '{routes[enum].output}'"
                f" for '{routes[enum]}' in '{routes}' at '{enum}'.",
            )
            #   endregion

        def test_wrapper(
            routes: router.ROUTES_TYPE,
            request_enum: EnumMeta,
            f: router.LambdaHandler,
            event: Dict[str, Any],
            context: Dict[str, Any],
        ) -> str:
            # region Assert rout dict and request enum
            self.assertTrue(
                routes and type(routes) is dict,
                f"{name}: Invalid routes dict: '{routes}'.",
            )
            self.assertTrue(
                request_enum
                and isinstance(request_enum, EnumMeta)
                and len(request_enum),
                f"{name}: Invalid request enum: '{request_enum}'.",
            )
            self.assertTrue(
                hasattr(request_enum, "__module__")
                and request_enum.__module__
                and request_enum.__module__ == f"{self.LAMBDA_FILE_NAME}",
                f"{name}: Incorrect request enum: '{request_enum}' not in '{self.LAMBDA_FILE_NAME}'.",
            )
            # endregion

            # region Assert that all entries in routes dict are valid
            for key in routes:
                self.assertTrue(
                    isinstance(key, Enum)
                    and type(key) is request_enum
                    and key in request_enum,
                    f"{name}: Invalid entry: '{key}' in '{routes}'"
                    f" not associated with '{request_enum}'.",
                )
                test_route(routes, key)
            # endregion

            # region Assert that all members of request enum have a route
            for key in request_enum:
                self.assertTrue(
                    key in routes,
                    f"{name}: Missing route: Enum '{key}' not in '{routes}'.",
                )
                test_route(routes, key)
            # endregion
            return ""

        with patch.object(router, "wrapper", new=test_wrapper):
            event = self.MOCK_USER_PACKET
            lambda_handler(event, None)
