from typing import Dict, Sequence, List
from os import path

from deployment_properties import DEFAULT_LAYER, PREFIX


def input_name(
    existing: Dict[str, str], default: str, deploy_type: str, action: str
) -> str:
    if action == "update":
        return input_to_update(existing, default, deploy_type)
    elif action == "new":
        return input_new(existing, default, deploy_type)
    else:
        print("Misuse of deployment_ui.input_name().")
        quit()


def input_to_update(existing: Dict[str, str], default: str, deploy_type: str) -> str:
    name = ""
    while not name or name not in existing.keys() and name not in existing.values():
        appendix = f" [{default}]" if default in existing else ""
        name = input(f"Name or ARN for {deploy_type} to update{appendix}: ").lower()
        if name == "" and default in existing.keys():
            name = default
    return name


def input_new(existing: Dict[str, str], default: str, deploy_type: str) -> str:
    name = ""
    while not name or name in existing.keys():
        appendix = f" [{default}]" if default not in existing.keys() else ""
        name = input(f"Name of new {deploy_type}{appendix}: ").lower()
        if name == "" and default not in existing.keys():
            name = default
        if name in existing.keys():
            abort = ""
            while abort not in ("y", "n"):
                abort = input(
                    f"Matched {deploy_type} '{name}' to existing {deploy_type} '{existing[name]}', abort? [y/n]"
                ).lower()
            if abort == "y":
                quit()
    return name


def input_zip_name() -> str:
    zip_name = ""
    while not path.exists(f"{zip_name}.zip"):
        zip_name = input("Name of zip-file without extension: ").lower()
    return zip_name


def input_action(actions: Sequence[str], tag: str) -> str:
    action = ""
    while action not in actions:
        action = input(f"{tag} [{'/'.join(actions)}]: ").lower()
    return action


def input_validate_new(
    existing: Dict[str, str], zip_name: str, deployment_type: str
) -> None:
    for entry in existing.keys():
        if zip_name in entry:
            abort = ""
            while abort not in ("y", "n"):
                abort = input(
                    f"Matched '{zip_name}' to existing {deployment_type} '{entry}', abort? [y/n]: "
                ).lower()
            if abort == "y":
                quit()


def input_zip_directory(default_zip_dir: str) -> str:
    directory = ""
    while not path.exists(directory):
        directory = input(f"Relative zip dir [{default_zip_dir}]: ").rstrip("/")
        if directory == "":
            directory = default_zip_dir
    return directory


def input_layers_for_function(layers: Dict[str, str]) -> List[str]:
    print(f"\nPrinting list of available layers.")
    for layer in layers:
        print(f"{layer} : {layers[layer]}")
    function_layers: List[str] = []
    user_input = ""
    while (
        len(function_layers) > 0
        and all(
            layer in layers.keys() or layer in layers.values()
            for layer in function_layers
        )
        or user_input == "none"
    ):
        default = f"{PREFIX}{DEFAULT_LAYER}"
        appendix = f" [{default}/none]" if default in layers.keys() else ""
        user_input = input(f"Layers for function{appendix}").lower().strip()
        function_layers = [_.strip() for _ in user_input.split(",")]
        if user_input == "":
            function_layers = [default]
    return function_layers
