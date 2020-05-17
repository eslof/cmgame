import boto3


# TODO: create cloudfront distributed s3 bucket for config data like ws url
def web_socket_endpoint():
    #  TODO: get live state
    return {"response_code": 200, "address": "domain.com/ws"}


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("cmgame")
