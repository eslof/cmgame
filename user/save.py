from country import Country
from properties import RequestField, UserAttr, TableKey
from properties import TablePartition, UserState, Constants
from internal import validate_field, RequestHandler, end, validate_request
from enum import Enum, unique, auto

from user import User


@unique
class SaveRequest(Enum):
    NAME = auto()
    FLAG = auto()
    META = auto()


class Save(RequestHandler):
    """User requests to save changes made to one of the user's settings or profile."""

    @staticmethod
    def run(event: dict, user_id: str) -> bool:
        """Set requested user property to requested value for given user id."""
        request = SaveRequest(event[RequestField.User.SAVE])
        attribute, value = None, None
        if request == SaveRequest.NAME:
            attribute, value = UserAttr.NAME, RequestField.User.NAME
        elif request == SaveRequest.FLAG:
            attribute, value = UserAttr.FLAG, RequestField.User.FLAG
        elif request == SaveRequest.META:
            attribute, value = UserAttr.META, RequestField.User.META
        return User.update(user_id, attribute, value)

    @staticmethod
    def validate(event) -> None:
        """Confirm name or meta to be of appropriate size or confirm existence of country."""
        req = validate_request(event, SaveRequest, RequestField.User.SAVE)
        field, validation, message = None, None, None
        if req == SaveRequest.NAME:
            field = RequestField.User.NAME
            validation = (
                lambda value: isinstance(value, str)
                and len(value) < Constants.User.NAME_MAX_LENGTH
            )
            message = "User Save API (NAME)"
        elif req == SaveRequest.FLAG:
            field = RequestField.User.FLAG
            validation = (
                lambda value: isinstance(value, int)
                and value in Country._value2member_map_
            )
            message = "User Save API (FLAG)"
        elif req == SaveRequest.META:
            field = RequestField.User.META
            validation = (
                lambda value: isinstance(value, str)
                and len(value) < Constants.User.META_MAX_LENGTH
            )
            message = "User Save API (META)"

        validate_field(event, field, validation, message)
