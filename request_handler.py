# TODO: metaclass=abc.ABCMeta ? research
from abc import ABC, abstractmethod
from typing import Any, no_type_check


class RequestHandler(ABC):
    # TODO:
    # def __new__(cls, *args, **kwargs) -> None:
    #    throw exception for architecture misuse
    #    return None

    @staticmethod
    @abstractmethod
    @no_type_check
    def run(event, user_id, valid_data) -> Any:
        pass

    @staticmethod
    @abstractmethod
    @no_type_check
    def validate(event, user_id):
        pass
