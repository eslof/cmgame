from typing import Dict, Any

from internal import validate_field
from properties import RequestField, Constants


class InternalHelper:
    @staticmethod
    def validate_grid_request(target: Dict[str, Any], message: str = "") -> None:
        validate_field(
            target=target,
            field=RequestField.Home.GRID,
            validation=lambda value: type(value) is int
            and 0 < value <= Constants.Home.SIZE
            and value != Constants.Home.MATCH_GRID_SLOT,
            message=message,
        )
