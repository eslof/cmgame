from abc import ABC, abstractmethod

# TODO: metaclass=abc.ABCMeta ? research


class RequestHandler(ABC):
    """Classes used by our AWS Lambda functions to handle requests inherit this ABC.
    This to help maintain the architecture of the application.
    Refer to RequestHandlerTemplate.py for new file templates."""

    @staticmethod
    @abstractmethod
    def validate(*args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def run(*args, **kwargs):
        pass
