from internal import end, RequestHandler
from item import Item
from random import Random


class Demand(RequestHandler):
    @staticmethod
    def run(inventory: list, seed: int) -> list:
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
    def sanitize(key_count: int) -> None:
        # TODO: does this really need to be here
        if key_count <= 0:
            end(f"Insufficient keys: {key_count}")
