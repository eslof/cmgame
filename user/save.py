from countries import Countries
from properties import RequestField, UserAttr, TableKey, TablePartition
from internal import validate_field, RequestHandler
from enum import Enum, unique, auto


@unique
class SaveRequest(Enum):
    NAME = auto()
    FLAG = auto()
    META = auto()


class Save(RequestHandler):
    @staticmethod
    def run(save_request: int, user_id: str, event: dict) -> bool:
        # TODO: this could probably be made better
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
                ConditionExpression=f"attribute_exists(#id)",
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="UPDATED_NEW",
            )
        except ClientError as e:
            return False  # TODO: error handling
            #  error = e.response['Error']['Code']
            # if error != 'ConditionalCheckFailedException':
            #     end("Error: " + error)

            # end("No such user found!")
        else:
            return True

    @staticmethod
    def validate(event) -> None:
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
                and value in Countries._value2member_map_,
                "User Save API (FLAG)",
            )
        elif save_req == SaveRequest.META:
            validate_field(
                event,
                RequestField.User.META,
                lambda value: isinstance(value, str) and len(value) < 2048,
                "User Save API (META)",
            )
