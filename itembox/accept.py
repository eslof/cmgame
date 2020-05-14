from properties import RequestField
from internal import validate_field, RequestHandler


class Accept(RequestHandler):
    """User responds to a demanded itembox with requested choice."""

    @staticmethod
    def run(user_id, choice):
        """Add item id that corresponds to the choice in current demanded itembox."""
        # TODO: implement
        pass

    @staticmethod
    def validate(event):
        """Confirm that the choice made is in range of the item count presented in an itembox."""
        validate_field(
            target=event,
            field=RequestField.ItemBox.CHOICE,
            validation=lambda value: isinstance(value, int) and 1 <= value <= 3,
            message="ItemBox Accept API",
        )
