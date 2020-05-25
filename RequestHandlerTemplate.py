from typing import Any


#set($camel_case_name = ${StringUtils.removeUnderScores($NAME)})
#set($desc = $description)
#set($empty = $desc.replace(" ", ""))
#if($empty == "")
    #set($desc = "${camel_case_name} implementation.")
#end


class $camel_case_name(RequestHandler):
    """TODO:${desc}"""

    @staticmethod
    @typing.no_type_check
    def run(event, user_id, valid_data) -> Any:
        """TODO:${camel_case_name}.run implementation."""
        pass

    @staticmethod
    @typing.no_type_check
    def validate(event, user_id) -> Any:
        """TODO:${camel_case_name}.validate implementation."""
        pass
