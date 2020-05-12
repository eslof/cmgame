from properties import TableKey, TablePartition, HomeAttr, RequestField
from internal import sanitize_json


class Save:
    @staticmethod
    def run(home_id: str, meta_data: str):
        try:
            # TODO: rework database model
            response = table.update_item(
                Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: home_id},
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
    def sanitize(event):
        # TODO: Make sure it's not too big meta content
        sanitize_json(
            target=event, field=RequestField.Home.META, sanity_id="Home Save API"
        )
