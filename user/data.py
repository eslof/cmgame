from item import Item
from properties import (
    TableKey,
    TablePartition,
    UserAttr,
    ResponseField,
    HomeAttr,
    ItemAttr,
)
from internal import end, RequestHandler
from user import User


class Data(RequestHandler):
    """Returning user requests a welcome package containing: Profile, inventory, home names and their biodomes."""

    @staticmethod
    def validate():
        """TODO: figure out what to do here since we're already auth'd"""
        pass

    @staticmethod
    def run(user_id: str) -> dict:
        """Get and return name, flag, meta-data, inventory, and home list for given user id."""
        try:
            attributes = [
                UserAttr.NAME,
                UserAttr.FLAG,
                UserAttr.META,
                UserAttr.HOMES,
                UserAttr.INVENTORY,
            ]

            response = User.get(user_id=user_id, attributes=", ".join(attributes))

        except ClientError as e:
            end(e.response["Error"]["Message"])  # TODO: Proper error-handling
            # this avoids complains about unassigned reference to response_item
            return {}
        else:
            if "Item" not in response or len(response["Item"] < 1):
                end("No such user found")  # TODO: Proper error-handling

            response_item = response["Item"][0]

        user_data = {
            ResponseField.User.NAME: response_item[UserAttr.NAME],
            ResponseField.User.FLAG: response_item[UserAttr.FLAG],
            ResponseField.User.META: response_item[UserAttr.META],
            ResponseField.User.HOMES: {
                key: value
                for key, value in response_item[UserAttr.HOMES].items()
                if key == HomeAttr.BIODOME or key == HomeAttr.NAME
            },
            ResponseField.User.INVENTORY: [
                Item.get_template(value) for value in response_item[UserAttr.INVENTORY]
            ],
        }

        return user_data
