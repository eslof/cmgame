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
    def run(save_request: int, user_id: str, event: dict) -> bool:
        """TODO: this needs to be reworked"""

        request = SaveRequest(save_request)
        expression_names = {}
        expression_values = {}
        if request == SaveRequest.NAME:
            expression_values[":value"] = event[RequestField.User.NAME]
            expression_names["#name"] = {"S": UserAttr.NAME}
        elif request == SaveRequest.FLAG:
            expression_values[":value"] = event[RequestField.User.FLAG]
            expression_names["#name"] = {"N": UserAttr.FLAG}
        elif request == SaveRequest.META:
            expression_values[":value"] = event[RequestField.User.META]
            expression_names["#name"] = {"S": UserAttr.META}

        expression_names["#id"] = TableKey.PARTITION

        try:
            # TODO: rework database model
            response = table.update_item(
                Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
                UpdateExpression="set #name = :value",
                ConditionExpression=f"attribute_exists(#id) AND user_state <> {UserState.BANNED.value}",
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            if error != "ConditionalCheckFailedException":
                end("Error: " + error)
            # TODO: figure out if we tell the client he's banned or whatever
            return False
        else:
            return True

    @staticmethod
    def validate(event) -> None:
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
