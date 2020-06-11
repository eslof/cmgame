from typing import Dict, Any, TypedDict, Callable, List

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


class DeployFunction(TypedDict):
    new: Callable[[str, str, List[str]], Dict[str, Any]]
    update: Callable[[str, str, List[str]], Dict[str, Any]]


class DeployLayer(TypedDict):
    new: Callable[[str, str], Dict[str, Any]]
    update: Callable[[str, str], Dict[str, Any]]


class DeployRoute(TypedDict):
    function: DeployFunction
    layer: DeployLayer
