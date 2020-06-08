from typing import no_type_check, Dict

from config import Config
from database import db_update
from db_properties import TableKey, TablePartition, UserAttr, HomeAttr
from internal import validate_meta, end
from properties import RequestField
from request_handler import RequestHandler
from user_utils import User


class Save(RequestHandler):
    @staticmethod
    @no_type_check
    def run(event, user_id, valid_data) -> bool:
        home_id = valid_data[UserAttr.CURRENT_HOME]
        meta_data = event[RequestField.Home.META]
        if not db_update(
            Key={TableKey.PARTITION: TablePartition.HOME, TableKey.SORT: home_id},
            UpdateExpression=f"SET #meta = :home_meta",
            ConditionExpression=f"attribute_exists(#id)",
            ExpressionAttributeNames={"#id": TableKey.SORT, "#meta": HomeAttr.META,},
            ExpressionAttributeValues={":home_meta": meta_data},
        ):
            end("Unable to save home meta.")
        return True

    @staticmethod
    @no_type_check
    def validate(event, user_id) -> Dict[str, str]:
        user_data = User.get(user_id, UserAttr.CURRENT_HOME)
        if not user_data:
            end("Unable to retrieve current home for user.")
        validate_meta(
            target=event,
            field=RequestField.Home.META,
            max_size=Config.HOME_META_LIMIT,
            message="Home Save API (META)",
        )
        return user_data
