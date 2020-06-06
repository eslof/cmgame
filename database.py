from functools import wraps
from typing import Dict, Union, no_type_check, Any, Optional

# import sqlite3
import boto3  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

from db_properties import AWSError, RateException
from internal import end
from view import View


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
            raise RateException(
                View.error(RateException.__name__, e.response["Error"]["Code"])
            )
        return False
    except Exception as e:
        end(f"Unknown error ({type(e).__name__}).")  # todo: think about this one
    else:
        return response or True


def db_scan(*args, **kwargs) -> Optional[Dict[str, Any]]:
    response = _db_try(table.scan, lambda v: None, args, kwargs)
    return response.get("Items", None)


def db_update(*args, **kwargs) -> bool:
    return _db_try(table.update_item, lambda v: False, args, kwargs)


def db_get(*args, **kwargs) -> Optional[Dict[str, Any]]:
    response = _db_try(table.get_item, lambda v: None, args, kwargs)
    return response.get("Item", None)


def db_put(*args, **kwargs) -> bool:
    return _db_try(table.put_item, lambda e: False, args, kwargs)


def db_delete(*args, **kwargs) -> bool:
    return _db_try(table.delete, lambda v: False, args, kwargs)
