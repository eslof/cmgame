from typing import Protocol, Dict, Any, TypedDict, Callable

# region CMGame
FUNCTIONS = ["home", "item", "itembox", "match", "user", "test"]
PREFIX = "cmgame-"
DEFAULT_LAYER = "layer"
DEFAULT_LAYERS = [f"{PREFIX}{DEFAULT_LAYER}"]
DEFAULT_ZIP_DIR = "../bin"
# endregion
# region AWS
ROLE = "cmgame"
RUNTIME = "python3.8"
# endregion


class DeployRoute(TypedDict):
    new: Callable[[str, str], Dict[str, Any]]
    update: Callable[[str, str], Dict[str, Any]]
