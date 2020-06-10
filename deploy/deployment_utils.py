from os import path
from typing import Dict, Any, Optional, Callable

import boto3  # noqa
from botocore.exceptions import ClientError  # noqa

from deployment_ui import input_layers_for_function

LAMBDA_CLIENT = boto3.client("lambda")


def lambda_try(
    lambda_function: Callable[..., Any], *args: Any, **kwargs: Any
) -> Optional[Dict[str, Any]]:
    try:
        results = lambda_function(*args, **kwargs)
    except ClientError as e:
        print(e)
        return None
    except Exception:
        return None
    else:
        return results or {}


def data_try(zip_name: str, tag: str) -> bytes:
    file_name = f"{zip_name}.zip"
    if not path.exists(file_name):
        print(f"({tag}) File not found: {file_name}.")
        quit()
    try:
        with open(file_name, "rb") as file_binary:
            data = file_binary.read()
    except IOError as e:
        print(f"({tag}) IOError when open/read: {file_name}: {e}.")
        quit()
    if not data or len(data) <= 0:
        print(f"({tag}) Data missing or empty: {file_name}.")
        quit()
    return data


def get_layers() -> Dict[str, str]:
    results = lambda_try(LAMBDA_CLIENT.list_layers)
    if results is None:
        print("Unable to get live layers.")
        quit()
    if "Layers" not in results or not all(
        all(key in layer.keys() for layer in results["Layers"])
        for key in ("LayerName", "LayerArn")
    ):
        print(f"Unexpected results: {results}")
        quit()
    layers = results["Layers"]
    if len(layers) == 0:
        print("List of live layers returned empty.")
    return {layer["LayerName"]: layer["LayerArn"] for layer in layers}


def get_functions() -> Dict[str, str]:
    results = lambda_try(LAMBDA_CLIENT.list_functions)
    if results is None:
        print("Unable to get live functions.")
        quit()
    if "Functions" not in results or not all(
        all(key in function.keys() for function in results["Functions"])
        for key in ("FunctionName", "FunctionArn")
    ):
        print(f"Unexpected results: {results}")
        quit()
    functions = results["Functions"]
    if len(functions) == 0:
        print("List of live functions returned empty.")
    return {function["FunctionName"]: function["FunctionArn"] for function in functions}


def get_list(deployment_type: str) -> Dict[str, str]:
    if deployment_type == "function":
        return get_functions()
    elif deployment_type == "layer":
        return get_layers()
    else:
        print("Misuse of deployment_utils.get_list().")
        quit()


def publish_layer(function_name: str, zip_name: str) -> Dict[str, Any]:
    data = data_try(zip_name, "Layer")
    print("Success!")
    return "SomeArn"
    # results = lambda_try(
    #     LAMBDA_CLIENT.publish_layer_version,
    #     LayerName=name,
    #     Content={"ZipFile": data},
    #     CompatibleRuntimes=["python3.8"],
    # )
    # if results is None:
    #     print(f"Unable to publish layer: {name}.")
    #     quit()
    # if "LayerArn" not in results:
    #     print(f'Unexpected results: "LayerArn" not in {results}')
    #     quit()
    # return results["LayerArn"]  # type: str


# region Not done
def update_function(function_name: str, zip_name: str) -> Dict[str, Any]:
    data = data_try(zip_name, "Function")
    print("Success!")
    # return LAMBDA_CLIENT.update_function_code(FunctionName=name, ZipFile=data)


def create_function(function_name: str, zip_name: str) -> Dict[str, Any]:
    layers = get_layers()
    if len(layers) <= 0:
        data = data_try(zip_name, "Function")
        return {"FunctionName": function_name, "FunctionArn": "string"}

    function_layers = input_layers_for_function(layers)
    data = data_try(zip_name, "Function")
    print("Success!")
    # return LAMBDA_CLIENT.create_function(
    #     FunctionName=function_name,
    #     Runtime=RUNTIME,
    #     Role=ROLE,
    #     Handler="lambda_handler",
    #     Code={"ZipFile": data},
    #     Layers=function_layers,
    # )
