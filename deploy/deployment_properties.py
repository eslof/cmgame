from typing import Protocol, Dict, Any, TypedDict, Callable

LAYER = "layer"
DEFAULT_ZIP_DIR = "../bin"
FUNCTIONS = ["home", "item", "itembox", "match", "user", "test"]
# FUNCTIONS = input("Functions to update (csv): ").split(",")
PREFIX = "cmgame-"


class LambdaDeploy(Protocol):
    def __call__(self, lambda_name: str, zip_file: str) -> Dict[str, Any]:
        ...


class DeployRoute(TypedDict):
    new: Callable[[str, str], Dict[str, Any]]
    update: Callable[[str, str], Dict[str, Any]]
