from properties import RequestField
from internal import validate_field, RequestHandler


class Accept(RequestHandler):
    @staticmethod
    def run(user_id, choice):
        # TODO: implement
        pass

    @staticmethod
    def validate(event):
        validate_field(
            target=event,
            field=RequestField.ItemBox.CHOICE,
            validation=lambda value: isinstance(value, int) and 1 <= value <= 3,
            validation_id="ItemBox Accept API",
        )
