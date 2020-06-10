from enum import Enum, unique, auto
from typing import no_type_check

from config import Config
from country import Country
from db_properties import UserAttr
from internal import validate_field, validate_request, validate_meta, end, validate_name
from properties import Constants, RequestField
from request_handler import RequestHandler
from user_utils import UserUtils


@unique
class SaveRequest(Enum):
    NAME = auto()
    FLAG = auto()
    META = auto()


class Save(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        request = SaveRequest(event[RequestField.User.SAVE])
        attribute, value = None, None
        if request == SaveRequest.NAME:
            attribute, value = UserAttr.NAME, RequestField.User.NAME
        elif request == SaveRequest.FLAG:
            attribute, value = UserAttr.FLAG, RequestField.User.FLAG
        elif request == SaveRequest.META:
            attribute, value = UserAttr.META, RequestField.User.META
        if not UserUtils.update(user_id, attribute, value):
            end("Unable to save user data.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id):
        req = validate_request(event, SaveRequest)
        if req == SaveRequest.NAME:
            validate_name(
                target=event,
                field=RequestField.User.NAME,
                max_length=Constants.User.NAME_MAX_LENGTH,
                message="User Save API (NAME)",
            )
        elif req == SaveRequest.FLAG:
            validate_request(event, Country, RequestField.User.FLAG)
        elif req == SaveRequest.META:
            validate_meta(
                target=event,
                field=RequestField.User.META,
                max_size=Config.USER_META_LIMIT,
                message="User Save API (META)",
            )
