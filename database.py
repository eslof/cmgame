import boto3
from botocore.exceptions import ClientError
import os


# TODO: create cloudfront distributed s3 bucket for config data like ws url
def web_socket_endpoint():
    #  TODO: get live state
    return {"response_code": 200, "address": "domain.com/ws"}


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cmgame")

# response = table.scan()
# print(response["Items"][0]["homes"][0]["biodome"])
