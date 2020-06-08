# TODO: metaclass=abc.ABCMeta ? research
from abc import ABC, abstractmethod
from typing import Any, no_type_check


class RequestHandler(ABC):
    @staticmethod
    @abstractmethod
    def run(event, user_id, valid_data) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def validate(event, user_id):
        pass
