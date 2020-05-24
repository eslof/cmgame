from typing import Optional, Union

from database import *
from properties import UserState
from request_handler import RequestHandler
from user_utils import User


class Find(RequestHandler):
    @staticmethod
    def run(event: dict, user_id: str, valid_data: dict) -> Union[str, bool]:
        # TODO: rework all of this
        user_state = UserState(valid_data[UserAttr.STATE])
        if user_state == UserState.MATCHED:
            return web_socket_endpoint()["address"]
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
        # TODO: error handling
        if len(response["Item"] > 0):
            # TODO: update listing's state to pending, and prompt for accept by finder
            # TODO: then as the enlisters code comes to update its enlistment we look for this
            # TODO: set match finder_id and send match_id to ws
            return web_socket_endpoint()["address"]
        return False

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> dict:
        user_data = User.get(user_id, UserAttr.STATE)
        return user_data
