from item import Item
from properties import (
    TableKey,
    TablePartition,
    UserAttr,
    ResponseField,
    HomeAttr,
    ItemAttr,
)
from internal import RequestHandler
from user import User


class Data(RequestHandler):
    """Returning user requests a welcome package containing: Profile, inventory, home names and their biodomes."""

    @staticmethod
    def validate():
        """TODO: figure out what to do here since we're already auth'd and ban check is built in"""
        pass

    @staticmethod
    def run(user_id: str) -> dict:
        """Get and return name, flag, meta-data, inventory, and home list for given user id."""
        attributes = [
            UserAttr.NAME,
            UserAttr.FLAG,
            UserAttr.META,
            UserAttr.HOMES,
            UserAttr.INVENTORY,
        ]
        user_data = User.get(user_id=user_id, attributes=", ".join(attributes))

        return {
            ResponseField.User.NAME: user_data[UserAttr.NAME],
            ResponseField.User.FLAG: user_data[UserAttr.FLAG],
            ResponseField.User.META: user_data[UserAttr.META],
            ResponseField.User.HOMES: {
                key: value
                for key, value in sorted(
                    user_data[UserAttr.HOMES].items(), key=UserAttr.Home.HOME_ID
                )
                if key == HomeAttr.BIODOME or key == HomeAttr.NAME
            },
            ResponseField.User.INVENTORY: [
                Item.get_template(value) for value in user_data[UserAttr.INVENTORY]
            ],
        }
