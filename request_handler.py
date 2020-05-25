# TODO: metaclass=abc.ABCMeta ? research
import typing
from abc import ABC, abstractmethod
from typing import Optional, Any, Dict


class RequestHandler(ABC):
    # TODO:
    # def __new__(cls, *args, **kwargs) -> None:
    #    throw exception for architecture misuse
    #    return None

    @typing.no_type_check
    @staticmethod
    @abstractmethod
    def run(event: Dict[str, Any], user_id: Optional[str], valid_data,) -> Any:
        pass

    @typing.no_type_check
    @staticmethod
    @abstractmethod
    def validate(event: Dict[str, Any], user_id: Optional[str]):
        pass
