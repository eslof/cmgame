from abc import ABC, abstractmethod
from typing import Optional, Any, Union, Dict, List


# TODO: metaclass=abc.ABCMeta ? research


class RequestHandler(ABC):
    """Classes used by our AWS Lambda functions to handle requests inherit this ABC.
    This to help maintain the architecture of the application.
    Refer to RequestHandlerTemplate.py for new file templates."""

    @staticmethod
    @abstractmethod
    def run(
        event: Dict[str, Any], user_id: Optional[str], valid_data: Optional[Any],
    ) -> Optional[Any]:
        pass

    @staticmethod
    @abstractmethod
    def validate(event: Dict[str, Any], user_id: Optional[str]) -> Optional[Any]:
        pass
