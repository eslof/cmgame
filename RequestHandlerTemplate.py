from typing import Optional, Any

from request_handler import RequestHandler
#set($camel_case_name = ${StringUtils.removeUnderScores($NAME)})

class $camel_case_name(RequestHandler):
    """$class_doc"""

    @staticmethod
    def run(event: dict, user_id: str, data: Any) -> Any:
        """$run_doc"""
        pass

    @staticmethod
    def validate(event: dict, user_id: str) -> Optional[dict]:
        """$validate_doc"""
        pass
