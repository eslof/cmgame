from base64 import b64encode
from encrypt import password_encrypt
from properties import RequestField, TableKey, HomeAttr, Secret, Constants, Biodome
from internal import sanitize_field, generate_id, end, RequestHandler


class New(RequestHandler):
    @staticmethod
    def run(user_id: str, name: str, biodome: int):
        new_id = generate_id()
        try:
            # TODO: rework database model
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
    def sanitize(event: dict) -> None:
        sanitize_field(
            target=event,
            field=RequestField.Home.NAME,
            sanity=lambda value: isinstance(value, str)
            and 0 < len(value) <= Constants.Home.NAME_MAX_SIZE,
            sanity_id="Home Create API (NAME)",
        )
        sanitize_field(
            target=event,
            field=RequestField.Home.BIODOME,
            sanity=lambda value: isinstance(value, int)
            and value in Biodome._value2member_map_,
            sanity_id="Home Create API (BIODOME)",
        )
