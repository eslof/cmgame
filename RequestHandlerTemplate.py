from typing import Optional, Any
from request_handler import RequestHandler
#set($camel_case_name = ${StringUtils.removeUnderScores($NAME)})
#set($desc = $description)
#set($empty = $desc.replace(" ", ""))
#if($empty == "")
    #set($desc = "${camel_case_name} implementation.")
#end


class $camel_case_name(RequestHandler):
    """TODO:${desc}"""

    @staticmethod
    def run(event: dict, user_id: Optional[str], data: Optional[Any]) -> Optional[Any]:
        """TODO:${camel_case_name}.run implementation."""
        pass

    @staticmethod
    def validate(event: dict, user_id: Optional[str]) -> Optional[Any]:
        """TODO:${camel_case_name}.validate implementation."""
        pass
