from abc import ABC, abstractmethod

# TODO: metaclass=abc.ABCMeta ? research


class RequestHandler(ABC):
    """Modules used by our AWS Lambda functions inherit this ABC.
    This to help maintain the architecture of the application.
    Refer to RequestHandlerTemplate.py"""

    @staticmethod
    @abstractmethod
    def validate(*args, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def run(*args, **kwargs):
        pass
