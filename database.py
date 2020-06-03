from functools import wraps
from typing import Dict, Union, no_type_check, Any, Optional, Callable

# import sqlite3
import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

from db_properties import AWSError
from internal import end
from view import View


def web_socket_endpoint() -> Dict[str, Union[str, int]]:
    #  TODO: get live state
    return {"response_code": 200, "address": "domain.com/ws"}


# with sqlite3.connect("db.sql") as conn:
#    cursor = conn.execute("query")
#   res = cursor.fetchall()


dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
table = dynamodb.Table("cmgame")


def _db_try(table_function, *args, **kwargs) -> Union[Dict[str, Any], bool]:
    try:
        response = table_function(*args, **kwargs)
    except ClientError as e:
        if e.response["Error"]["Code"] in (
            AWSError.RATE_LIMIT,
            AWSError.REQ_LIMIT,
            AWSError.WCU_LIMIT,
        ):
            raise RateException(View.error(e.response["Error"]["Code"]))
        return False
    except Exception as e:
        end(f"Unknown error ({type(e).__name__}).")  # todo: think about this one
    else:
        return response or True


class RateException(Exception):
    pass


@no_type_check
def db_scan(*args, **kwargs) -> Optional[Dict[str, Any]]:
    response = _db_try(table.scan, lambda v: None, args, kwargs)
    if "Item" not in response or len(response["Item"]) <= 0:
        return
    return response


# @no_type_check
# @wraps(table.update_item)
# def db_update_assert(*args, **kwargs) -> Dict[str, Any]:
#     return _db_try(table.update_item, end, args, kwargs)


@no_type_check
@wraps(table.update_item)
def db_update(*args, **kwargs) -> bool:
    return _db_try(table.update_item, lambda v: False, args, kwargs)


@no_type_check
@wraps(table.get_item)
def db_get(*args, **kwargs) -> Optional[Dict[str, Any]]:
    response = _db_try(table.get_item, lambda v: None, args, kwargs)
    if "Item" not in response or len(response["Item"]) <= 0:
        return
    return response


@no_type_check
@wraps(table.put_item)
def db_put(*args, **kwargs) -> bool:
    return _db_try(table.put_item, lambda e: False, args, kwargs)


@no_type_check
@wraps(table.put_item)
def db_delete(*args, **kwargs) -> bool:
    return _db_try(table.delete, lambda v: False, args, kwargs)
