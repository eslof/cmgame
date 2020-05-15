from country import Country
from properties import (
    TableKey,
    TablePartition,
    UserAttr,
    UserState,
    Secret,
    RequestField,
    QueueState,
    Constants,
)
from internal import validate_field, generate_id, end, RequestHandler
from encrypt import password_encrypt
from base64 import b64encode

from user import User


class New(RequestHandler):
    """We are blessed with a new user, make sure he has a good time.
    New user is added and receive: A list of starting items and a list of biodomes for a home."""

    @staticmethod
    def run(name: str, flag: int) -> str:
        """Generate new ID and push User.template_new with given name and flag into DB.
        Returns the user id on successful entry TODO: why cant dynamodb just give me an auto id"""
        new_id = generate_id()
        try:
            # TODO: rework database model
            response = table.put_item(
                Item=User.template_new(new_id=new_id, name=name, flag=flag),
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": TableKey.PARTITION},
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]
            if error != "ConditionalCheckFailedException":
                end("Error: " + error)  # TODO: error handling

            return New.run(name, flag)  # TODO: recursion limit

        return b64encode(password_encrypt(new_id, Secret.USER_ID)).decode("ascii")

    @staticmethod
    def validate(event) -> None:
        """Confirm name to be of appropriate length.
        Confirm country/flag to exist (yes we decide what countries exist, deal with it)."""
        validate_field(
            event,
            RequestField.User.NAME,
            lambda value: isinstance(value, str)
            and 0 < len(value) < Constants.User.NAME_MAX_LENGTH,
            "User New API (NAME)",
        )
        validate_field(
            event,
            RequestField.User.FLAG,
            lambda value: isinstance(value, int)
            and value in Country._value2member_map_,
            "User New API (FLAG)",
        )
