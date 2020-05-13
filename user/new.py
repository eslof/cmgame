from countries import Countries
from properties import (
    TableKey,
    TablePartition,
    UserAttr,
    UserState,
    Secret,
    RequestField,
)
from internal import sanitize_field, generate_id, end, RequestHandler
from encrypt import password_encrypt
from base64 import b64encode


class New(RequestHandler):
    @staticmethod
    def run(name: str, flag: int) -> str:
        new_id = generate_id()
        try:
            # TODO: rework database model
            response = table.put_item(
                Item={
                    TableKey.PARTITION: TablePartition.USER,
                    TableKey.SORT: new_id,
                    UserAttr.STATE: UserState.NEW,
                    UserAttr.INVENTORY: {"BS": []},
                    UserAttr.NAME: name,
                    UserAttr.FLAG: flag,
                    UserAttr.KEY_COUNT: 0,
                },
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            if error != "ConditionalCheckFailedException":
                end("Error: " + error)  # TODO: error handling

            return New.run(name, flag)

        return b64encode(password_encrypt(new_id, Secret.USER_ID)).decode("ascii")

    @staticmethod
    def sanitize(event) -> None:
        sanitize_field(
            event,
            RequestField.User.NAME,
            lambda value: isinstance(value, str) and 0 < len(value) < 24,
            "User New API (NAME)",
        )
        sanitize_field(
            event,
            RequestField.User.FLAG,
            lambda value: isinstance(value, int) and Countries.sanitize(value),
            "User New API (FLAG)",
        )
