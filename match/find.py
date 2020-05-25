from typing import no_type_check

from botocore.exceptions import ClientError

from database import *
from internal import end
from properties import UserState
from request_handler import RequestHandler
from user_utils import User


class Find(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> Union[str, bool]:
        # TODO: rework all of this
        user_state = UserState(valid_data[UserAttr.STATE])
        if user_state == UserState.MATCHED:
            return web_socket_endpoint()["address"]
        try:
            response = table.get_item(
                Key={TableKey.PARTITION: TablePartition.MATCH},
                # TODO: condition expression: state != matched
                ConditionExpression="#enlisted_id <> :user_id and #finder_id = :empty",
                ExpressionAttributeNames={
                    "#enlisted_id": MatchAttr.LISTER_ID,
                    "#finder_id": MatchAttr.FINDER_ID,
                },
                ExpressionAttributeValues={":user_id": user_id, ":empty": ""},
                ScanIndexForward=False,
                Limit=1,
            )
        except ClientError as e:
            end(e.response["Error"]["Code"])
        else:
            if len(response["Item"] > 0):
                # TODO: update listing's state to pending, and prompt for accept by finder
                # TODO: then as the enlisters code comes to update its enlistment we look for this
                # TODO: set match finder_id and send match_id to ws
                return web_socket_endpoint()["address"]
        return False

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, int]:
        user_data = User.get(user_id, UserAttr.STATE)
        return user_data
