from request_handler import RequestHandler
from properties import TableKey, TablePartition, HomeAttr, RequestField
from internal import validate_meta
from database import *


class Save(RequestHandler):
    """User requests to save meta data of the user's selected home."""

    @staticmethod
    def run(home_id: str, meta_data: str):
        """Set meta data for given home id."""
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
    def validate(event: dict):
        """Confirm that home meta-data follows correct format and TODO: apply size limitation in case of misuse."""
        validate_meta(
            target=event, field=RequestField.Home.META, message="Home Save API"
        )
