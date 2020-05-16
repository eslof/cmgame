from requesthandler import RequestHandler
#set($camel_case_name = ${StringUtils.removeUnderScores($NAME)})

class $camel_case_name(RequestHandler):
    """$camel_case_name documentation"""

    @staticmethod
    def run(*args, **kwargs):
        """Run documentation"""
        pass

    @staticmethod
    def validate(*args, **kwargs):
        """Validate documentation"""
        pass