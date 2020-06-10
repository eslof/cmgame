from functools import partial
from typing import Dict, Any, Optional

import boto3  # noqa
from botocore.exceptions import ClientError  # noqa

from db_properties import AWSError, RateException
from internal import end
from view import View


dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
table = dynamodb.Table("cmgame")
table.put_item()


def _db_try(table_function, *args, **kwargs) -> Optional[Dict[str, Any]]:  # noqa
    try:
        response = table_function(*args, **kwargs)
    except ClientError as e:
        error = e.response["Error"]["Code"]
        if error in (AWSError.RATE_LIMIT, AWSError.REQ_LIMIT, AWSError.WCU_LIMIT,):
            raise RateException(View.error(error, RateException.__name__))
        return None
    except Exception as e:
        end(f"Unknown error ({type(e).__name__}).")  # todo: think about this one
    return response  # noqa


db_scan = partial(_db_try, table.scan)
db_update = partial(_db_try, table.update_item)
db_get = partial(_db_try, table.get_item)
db_put = partial(_db_try, table.put_item)
db_delete = partial(_db_try, table.delete)
