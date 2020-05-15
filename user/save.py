from country import Country
from properties import RequestField, UserAttr, TableKey, TablePartition
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
            event,
            RequestField.User.SAVE,
            lambda value: isinstance(value, int)
            and value in SaveRequest._value2member_map_,
            "User Save API (REQUEST)",
        )

        save_req = SaveRequest(event[RequestField.User.SAVE])

        if save_req == SaveRequest.NAME:
            validate_field(
                event,
                RequestField.User.NAME,
                lambda value: isinstance(value, str) and len(value) < 24,
                "User Save API (NAME)",
            )
        elif save_req == SaveRequest.FLAG:
            validate_field(
                event,
                RequestField.User.FLAG,
                lambda value: isinstance(value, int)
                and value in Country._value2member_map_,
                "User Save API (FLAG)",
            )
        elif save_req == SaveRequest.META:
            validate_field(
                event,
                RequestField.User.META,
                lambda value: isinstance(value, str) and len(value) < 2048,
                "User Save API (META)",
            )
