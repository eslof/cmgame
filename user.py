from country import Country
from internal import validate_field, end
from properties import (
    RequestField,
    TableKey,
    TablePartition,
    Secret,
    Constants,
    UserState,
    QueueState,
    UserAttr,
)
from encrypt import password_decrypt


class User:
    @staticmethod
    def template_new(new_id: str, name: str, flag: int) -> dict:
        return {
            TableKey.PARTITION: TablePartition.USER,
            TableKey.SORT: new_id,
            UserAttr.STATE: UserState.NEW.value,
            UserAttr.QUEUE_STATE: QueueState.NONE.value,
            UserAttr.INVENTORY: {"SS": []},
            UserAttr.NAME: name,
            UserAttr.FLAG: flag,
            UserAttr.KEY_COUNT: Constants.User.STARTING_KEY_COUNT,
        }

    @staticmethod
    def validate_id(event: dict) -> str:
        """TODO: user authentication + store user state + queue state"""
        validate_field(
            target=event,
            field=RequestField.User.ID,
            validation=lambda value: isinstance(value, str)
            and len(value) == Constants.User.EXPECTED_ID_LENGTH,
            message="User authentication API",
        )

        return password_decrypt(
            token=event[RequestField.User.ID], password=Secret.USER_ID
        )

    @staticmethod
    def get(user_id: str, attributes: str) -> dict:
        """TODO: is this even useful shouldn't I grab this and cache it at auth()?"""
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
