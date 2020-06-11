from typing import Dict, Sequence, List
from os import path

from deployment_properties import DEFAULT_LAYER, PREFIX
from deployment_utils import LAMBDA_CLIENT, get_function_layers


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


def input_choice(choices: Sequence[str], tag: str) -> str:
    choice = ""
    while choice not in choices:
        choice = input(f"{tag} [{'/'.join(choices)}]: ").lower()
    return choice


def input_validate_new(
    existing: Dict[str, str], zip_name: str, deployment_type: str
) -> None:
    for entry in existing.keys():
        if zip_name in entry or zip_name in existing[entry]:
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


def print_lambda_data(lambda_data: Dict[str, str], tag: str) -> None:
    print(f"\nPrinting list of {tag}.")
    for entry in lambda_data:
        print(f"{entry} : {lambda_data[entry]}")


def input_layers_for_function_new(layers: Dict[str, str]) -> List[str]:
    # region Set up
    print_lambda_data(layers, "available layers")
    ret_layers: List[str] = []
    layer_names = layers.keys()
    layer_arns = layers.values()
    default = f"{PREFIX}{DEFAULT_LAYER}"
    # endregion
    while not (
        len(ret_layers) > 0
        and all(layer in layer_names or layer in layer_arns for layer in ret_layers)
    ):
        # region User input for function layers
        appendix = f" [{default}/none]" if default in layer_names else " [none]"
        user_input = (
            input(f"Layers for function by Name or ARN (csv){appendix}").lower().strip()
        )
        ret_layers = [_.strip() for _ in user_input.split(",")]
        # endregion
        # region Commands none/empty default
        if user_input == "":
            ret_layers = [default]
        if user_input == "none":
            return []
        # endregion
    return ret_layers


def input_layers_for_function_update(
    function_name: str, layers: Dict[str, str]
) -> List[str]:
    layer_names = list(layers.keys())
    layer_arns = list(layers.values())
    print_lambda_data(layers, "available layers")
    current_layers = get_function_layers(function_name)
    function_layers = {
        name: layers[name]
        for name in layer_names
        if any(layers[name] in arn for arn in current_layers.keys())
    }
    print_lambda_data(function_layers, "function's current layers")
    print()
    function_layer_names = list(function_layers.keys())
    default = ",".join(function_layer_names)
    ret_layers: List[str] = []
    appendix = (
        f" [{default}/none]"
        if all(layer in layer_names for layer in function_layer_names)
        else ""
    )
    while len(ret_layers) == 0 or not all(
        layer in layer_names or layer in layer_arns for layer in ret_layers
    ):
        user_input = (
            input(f"Layers for function by Name or ARN{appendix}: ").lower().strip()
        )
        ret_layers = [layer.strip() for layer in user_input.split(",")]
        if user_input == "":
            ret_layers = list(function_layers.keys())
        if user_input == "none":
            return []
    return ret_layers
