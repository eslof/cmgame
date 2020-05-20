from botocore.exceptions import ClientError

from database import table, TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_meta
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User


class Save(RequestHandler):
    """User requests to save meta data of the user's selected home."""

    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> bool:
        """Set meta data for given home id."""
        home_id = valid_data[UserAttr.CURRENT_HOME]
        meta_data = event[RequestField.Home.META]
        try:
            # TODO: rework database model
            response = table.update_item(
                Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
                UpdateExpression=f"SET #meta = :home_meta",
                ConditionExpression=f"attribute_exists(#id)",
                ExpressionAttributeNames={
                    "#id": TableKey.PARTITION,
                    "#meta": HomeAttr.META,
                },
                ExpressionAttributeValues={":home_meta": meta_data},
            )
        except ClientError as e:
            # TODO: error handling
            return False
            #  error = e.response['Error']['Code']
            # if error != 'ConditionalCheckFailedException':
            #     end("Error: " + error)
            # end("No such user found!")
        else:
            return True

    @staticmethod
    def validate(event: dict, user_id: str) -> dict:
        """Confirm that home meta-data follows correct format and TODO: apply size limitation in case of misuse."""
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        validate_meta(
            target=event, field=RequestField.Home.META, message="Home Save API (META)"
        )
        return user_data
