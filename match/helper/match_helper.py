from datetime import datetime

from boto3.dynamodb.conditions import Attr

from database import db_get, db_scan, db_delete, db_update, db_put
from db_properties import TableKey, TablePartition, MatchAttr
from properties import Constants


class MatchHelper:
    @staticmethod
    def get_age(match_id: str) -> float:
        time_now = datetime.now()
        list_time_str = match_id[: -Constants.EXPECTED_ID_LEN]
        year_str = time_now.strftime("%Y-")
        list_time = datetime.strptime(f"{year_str}{list_time_str}", "%Y-%m-%d-%H-%M-%S")
        return (time_now - list_time).total_seconds()

    @staticmethod
    def find_available(user_id):
        return db_scan(
            Key={TableKey.PARTITION: TablePartition.MATCH},
            FilterExpression=Attr(MatchAttr.LISTER_ID).ne(user_id)
            & Attr(MatchAttr.FINDER_ID).eq(""),
            ScanIndexForward=False,
            Limit=1,
        )

    @staticmethod
    def delete(match_id):
        return db_delete(
            Key={TableKey.PARTITION: TablePartition.MATCH, TableKey.SORT: match_id,}
        )

    @staticmethod
    def claim(match_id, user_id):
        return db_update(
            Key={TableKey.PARTITION: TablePartition.MATCH, TableKey.SORT: match_id,},
            UpdateExpression="SET #finder_id = :user_id",
            ConditionExpression=f"attribute_exists(#id) AND #finder_id = :empty",
            ExpressionAttributeValues={":user_id": user_id, ":empty": ""},
            ExpressionAttributeNames={
                "#id": TableKey.SORT,
                "#finder_id": MatchAttr.FINDER_ID,
            },
        )

    @staticmethod
    def template_new(match_id, user_id):
        return {
            TableKey.PARTITION: TablePartition.MATCH,
            TableKey.SORT: match_id,
            MatchAttr.LISTER_ID: user_id,
            MatchAttr.FINDER_ID: "",
        }

    @classmethod
    def new(cls, new_id, user_id):
        return db_put(
            Item=cls.template_new(new_id, user_id),
            ConditionExpression="attribute_not_exists(#id)",
            ExpressionAttributeNames={"#id": TableKey.SORT},
        )

    @staticmethod
    def generate_id(user_id):
        return f"{datetime.now().strftime('%m-%d-%H-%M-%S')}{user_id}"

    @staticmethod
    def upsert_return(match_id, new_id):
        return db_update(
            Key={TableKey.PARTITION: TablePartition.MATCH, TableKey.SORT: match_id},
            UpdateExpression="SET #sort = :new_match_id",
            ExpressionAttributeNames={"#sort": TableKey.SORT,},
            ExpressionAttributeValues={":new_match_id": new_id,},
            ReturnValues="ALL_NEW",
        )
