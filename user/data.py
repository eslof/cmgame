import item
from properties import (
    TableKey,
    TablePartition,
    UserAttr,
    ResponseField,
    HomeAttr,
    ItemAttr,
)
from internal import end


class Data:
    @staticmethod
    def run(user_id: str) -> dict:
        try:
            # TODO: rework database model
            response = table.get_item(
                Key={TableKey.PARTITION: TablePartition.USER, TableKey.SORT: user_id},
                ProjectionExpression="#name, #flag, #meta, #inventory, #homes",
                ExpressionAttributeNames={
                    "#name": UserAttr.NAME,
                    "#flag": UserAttr.FLAG,
                    "#meta": UserAttr.META,
                    "#inventory": UserAttr.HOME_LIST,
                    "#homes": UserAttr.INVENTORY,
                },
            )
        except ClientError as e:
            end(e.response["Error"]["Message"])  # TODO: Proper error-handling
            return (
                {}
            )  # this avoids complains about unassigned reference to response_item return var
        else:
            if "Item" not in response:
                end("No such user found")  # TODO: Proper error-handling
            response_item = response["Item"]

        # TODO: clean this mess up
        user_data = {
            ResponseField.User.NAME: response_item.Name,
            ResponseField.User.FLAG: response_item.Flag,
        }

        item_ids = response_item.Inventory

        home_ids = []
        for home in response_item.Homes:
            home_id_entry = {
                TableKey.PARTITION: TablePartition.HOME,
                TableKey.SORT: home,
            }
            home_ids.append(home_id_entry)

        homes = []
        if home_ids:
            try:
                response = table.batch_get_item(home_ids)
            except ClientError as e:
                end(e.response["Error"]["Message"])  # TODO: Proper error-handling
                return (
                    {}
                )  # this avoids complains about unassigned reference to response_items return var
            else:
                # first (and only) table (index 0)
                if (
                    "Responses" not in response
                    or not response["Responses"]
                    or not response["Responses"][0]
                ):
                    end("No such homes found")

            # first (and only) table (index 0)
            response_items = response["Responses"][0]

            for item in response_items:
                home_entry = {
                    ResponseField.Home.NAME: item[HomeAttr.NAME],
                    ResponseField.Home.BIODOME: item[HomeAttr.BIODOME],
                }
                homes.append(home_entry)

        inventory = []
        if item_ids:
            for item_id in item_ids:
                item = item.get(item_id)
                inventory_entry = {
                    ResponseField.Item.BUNDLE: item[ItemAttr.BUNDLE],
                    ResponseField.Item.VERSION: item[ItemAttr.VERSION],
                }
                inventory.append(inventory_entry)

        user_data[ResponseField.User.HOMES] = homes
        user_data[ResponseField.User.INVENTORY] = inventory

        return user_data
