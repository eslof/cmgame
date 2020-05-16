import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cmgame")

# response = table.scan()
# print(response["Items"][0]["homes"][0]["biodome"])
