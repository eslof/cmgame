from country import Country
from properties import RequestField, UserAttr, TableKey
from properties import TablePartition, UserState, Constants
from internal import validate_field, RequestHandler, end
from enum import Enum, unique, auto


@unique
class SaveRequest(Enum):
    NAME = auto()
    FLAG = auto()
    META = auto()


class Save(RequestHandler):
    """User requests to save changes made to one of the user's settings or profile."""

    @staticmethod
    def run(request: Enum, user_id: str, event: dict) -> bool:
        """TODO: this needs to be reworked"""

        attr, value = None, None
        if request == SaveRequest.NAME:
            value = event[RequestField.User.NAME]
            attr = {"S": UserAttr.NAME}
        elif request == SaveRequest.FLAG:
            value = event[RequestField.User.FLAG]
            attr = {"N": UserAttr.FLAG}
        elif request == SaveRequest.META:
            value = event[RequestField.User.META]
            attr = {"S": UserAttr.META}

        try:
            # TODO: rework database model
            response = table.update_item(
                Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
                UpdateExpression="set #name = :value",
                ConditionExpression=f"attribute_exists(#id) AND #state <> :banned",
                ExpressionAttributeValues={
                    ":value": value,
                    ":banned": UserState.BANNED.value,
                },
                ExpressionAttributeNames={
                    "#name": attr,
                    "#id": TableKey.PARTITION,
                    "#state": UserAttr.STATE,
                },
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            if error != "ConditionalCheckFailedException":
                end("Error: " + error)
            # TODO: figure out if we tell the client he's banned or whatever
            # TODO: if we remove attribute_exists(#id) can we then just check
            #  if returned item count is zero to know explicitly if he's banned?
            return False
        else:
            return True

    @staticmethod
    def validate(event) -> SaveRequest:
        """Confirm that the request is valid and TODO: look over this"""

        validate_field(
            target=event,
            field=RequestField.User.SAVE,
            validation=lambda value: isinstance(value, int)
            and value in SaveRequest._value2member_map_,
            message="User Save API (REQUEST)",
        )

        save_req = SaveRequest(event[RequestField.User.SAVE])
        field, validation, message = None, None, None
        if save_req == SaveRequest.NAME:
            field = RequestField.User.NAME
            validation = (
                lambda value: isinstance(value, str)
                and len(value) < Constants.User.NAME_MAX_LENGTH
            )
            message = "User Save API (NAME)"
        elif save_req == SaveRequest.FLAG:
            field = RequestField.User.FLAG
            validation = (
                lambda value: isinstance(value, int)
                and value in Country._value2member_map_
            )
            message = "User Save API (FLAG)"
        elif save_req == SaveRequest.META:
            field = RequestField.User.META
            validation = (
                lambda value: isinstance(value, str)
                and len(value) < Constants.User.META_MAX_LENGTH
            )
            message = "User Save API (META)"

        validate_field(event, field, validation, message)
        return save_req
