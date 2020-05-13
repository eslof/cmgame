from internal import validate_field, end
from properties import RequestField, TableKey, TablePartition, Secret, Constants
from encrypt import password_decrypt


class User:
    @staticmethod
    def auth(event: dict) -> str:
        validate_field(
            target=event,
            field=RequestField.User.ID,
            validation=lambda value: isinstance(value, str)
                                     and len(value) == Constants.User.EXPECTED_ID_LENGTH,
            validation_id="User authentication API",
        )

        return password_decrypt(
            token=event[RequestField.User.ID], password=Secret.USER_ID
        )

    @staticmethod
    def get(user_id: str, attributes: str) -> dict:
        try:
            # TODO: rework db
            response = table.get_item(
                Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
                ProjectionExpression=attributes,
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            end("Error: " + error)
        else:
            if len(response["Item"]) == 0:
                end("Unable to find user for given UUID.")

            return response["Item"]
