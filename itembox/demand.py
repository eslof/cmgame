from random import Random

from request_handler import RequestHandler
from item import Item
from internal import end


class Demand(RequestHandler):
    """User demands an itembox, this is the part where we sell our souls for money."""

    @staticmethod
    def run(inventory: list, seed: int) -> list:
        """Produce a count of items for the user to choose between.
        We do not present the user with items he has already unlocked."""
        # TODO: whatever's going on here might not work
        Item.load()
        item_ids = list(Item.data.keys())
        Random(seed).shuffle(item_ids)
        filtered_list = list(set(item_ids) - set(inventory))
        choices = []
        # TODO: generators/comprehension? and maybe memory conservative with iterator?
        for i in range(3):
            if len(filtered_list) - len(inventory) > 0:
                choices.append(Item.data[filtered_list.pop(0)])

        return choices

    @staticmethod
    def validate(key_count: int) -> None:
        """Confirm that the user has the amount of keys needed for an itembox."""
        # TODO: does this really need to be here
        if key_count <= 0:
            end(f"Insufficient keys: {key_count}")
