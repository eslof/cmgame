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
                UserAttr.HOME_INFO,
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

            response_item = response["Item"]

        # TODO: clean this mess up
        user_data = {
            ResponseField.User.NAME: response_item.Name,
            ResponseField.User.FLAG: response_item.Flag,
        }

        item_ids = response_item.Inventory

        inventory = []
        if item_ids:
            for item_id in item_ids:
                item = Item.get(item_id)
                inventory_entry = {
                    ResponseField.Item.BUNDLE: item[ItemAttr.BUNDLE],
                    ResponseField.Item.VERSION: item[ItemAttr.VERSION],
                }
                inventory.append(inventory_entry)

        user_data[ResponseField.User.HOMES] = homes
        user_data[ResponseField.User.INVENTORY] = inventory

        return user_data
