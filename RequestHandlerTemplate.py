from request_handler import RequestHandler
#set($camel_case_name = ${StringUtils.removeUnderScores($NAME)})

class $camel_case_name(RequestHandler):
    """$class_doc"""

    @staticmethod
    def run(*args, **kwargs):
        """$run_doc"""
        pass

    @staticmethod
    def validate(*args, **kwargs):
        """$validate_doc"""
        pass