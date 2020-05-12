from properties import RequestField
from internal import sanitize_field


class Accept:
    @staticmethod
    def run(user_id, choice):
        # TODO: implement
        pass

    @staticmethod
    def sanitize(event):
        sanitize_field(
            target=event,
            field=RequestField.ItemBox.CHOICE,
            sanity=lambda value: isinstance(value, int) and 1 <= value <= 3,
            sanity_id="ItemBox Accept API",
        )
