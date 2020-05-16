from country import Country
from properties import Secret, RequestField, Constants
from internal import validate_field, end, RequestHandler
from encrypt import password_encrypt
from base64 import b64encode
from user import User


class New(RequestHandler):
    """We are blessed with a new user, make sure he has a good time.
    New user is added and receive: A list of starting items and a list of biodomes for a home."""

    @staticmethod
    def run(name: str, flag: int) -> str:
        """Generate new ID and push User.template_new with given name and flag into DB.
        Returns the user id on successful entry TODO: why cant dynamodb just give me an auto id"""
        new_id = ""
        max_attempts = 5
        while not new_id and max_attempts > 0:
            new_id = User.attempt_new(name, flag)
            max_attempts -= 1

        if not new_id:
            end("Unable to successfully create new user")

        return b64encode(password_encrypt(new_id, Secret.USER_ID)).decode("ascii")

    @staticmethod
    def validate(event) -> None:
        """Confirm name to be of appropriate length.
        Confirm country/flag to exist (yes we decide what countries exist, deal with it)."""
        validate_field(
            target=event,
            field=RequestField.User.NAME,
            validation=lambda value: isinstance(value, str)
            and 0 < len(value) < Constants.User.NAME_MAX_LENGTH,
            message="User New API (NAME)",
        )
        validate_field(
            target=event,
            field=RequestField.User.FLAG,
            validation=lambda value: isinstance(value, int)
            and value in Country._value2member_map_,
            message="User New API (FLAG)",
        )
