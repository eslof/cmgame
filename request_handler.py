from abc import ABC, abstractmethod
from typing import Optional, Any, Dict


# TODO: metaclass=abc.ABCMeta ? research


class RequestHandler(ABC):
    # TODO:
    # def __new__(cls, *args, **kwargs) -> None:
    #    throw exception for architecture misuse
    #    return None

    @staticmethod
    @abstractmethod
    def run(
        event: Dict[str, Any], user_id: Optional[str], valid_data: Optional[Any],
    ) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def validate(event: Dict[str, Any], user_id: Optional[str]) -> Optional[Any]:
        pass
