from base64 import b64encode
from encrypt import password_encrypt

from properties import RequestField, TableKey, HomeAttr, Secret, Constants, Biodome
from internal import validate_field, generate_id, end, RequestHandler


class New(RequestHandler):
    """User requests to create a new home."""

    @staticmethod
    def run(user_id: str, name: str, biodome: int):
        """TODO: this entire thing needs a rework: there need be a template for user item
        TODO: should it be recursive or is there a better way?"""

        new_id = generate_id()
        try:
            # TODO: rework database model template..
            response = table.put_item(
                Item={
                    TableKey.PARTITION: {"S": new_id},
                    HomeAttr.NAME: {"S": name},
                    HomeAttr.BIODOME: {"N": biodome},
                    HomeAttr.ITEM_GRID: {"M": {}},
                    HomeAttr.ITEM_META: {"M": {}},
                },
                ConditionExpression="attribute_not_exists(#id)",
                ExpressionAttributeNames={"#id": {"S": TableKey.PARTITION}},
            )
        except ClientError as e:
            error = e.response["Error"]["Code"]  # TODO: error handling
            if error == "ConditionalCheckFailedException":
                return New.run(user_id=user_id, name=name, biodome=biodome)
            end(error)
        else:
            return b64encode(password_encrypt(new_id, Secret.USER_ID)).decode("ascii")

    @staticmethod
    def validate(event: dict) -> None:
        """Confirm name to be of appropriate length, and existence of requested Biodome."""
        validate_field(
            target=event,
            field=RequestField.Home.NAME,
            validation=lambda value: isinstance(value, str)
            and 0 < len(value) <= Constants.Home.NAME_MAX_SIZE,
            message="Home Create API (NAME)",
        )
        validate_field(
            target=event,
            field=RequestField.Home.BIODOME,
            validation=lambda value: isinstance(value, int)
            and value in Biodome._value2member_map_,
            message="Home Create API (BIODOME)",
        )
