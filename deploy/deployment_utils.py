from os import path
from typing import Dict, Any, Optional, Callable, Tuple

import boto3
from botocore.exceptions import ClientError

from deployment_properties import ZIP_DIRECTORY

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


def data_try(directory: str, name: str, tag: str) -> bytes:
    file_path = f"../{directory}/{name}.zip"
    if not path.exists(file_path):
        print(f"({tag}) File not found: {file_path}.")
        quit()
    try:
        with open(file_path, "rb") as file_binary:
            data = file_binary.read()
    except IOError as e:
        print(f"({tag}) IOError when open/read: {file_path}: {e}.")
        quit()
    if not data or len(data) <= 0:
        print(f"({tag}) Data missing or empty: {file_path}.")
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


def publish_layer(name: str) -> str:
    print(f"Publishing layer: {name}")
    data = data_try(ZIP_DIRECTORY, name, "Layer")
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
def update_function(name: str) -> Dict[str, Any]:
    print(f"Updating function: {name}")
    data = data_try(ZIP_DIRECTORY, name, "Function")
    print("Success!")
    # return LAMBDA_CLIENT.update_function_code(FunctionName=name, ZipFile=data)


def create_function(name: str, layer_arn: str) -> Dict[str, Any]:
    print(f"Creating function: {name}")
    data = data_try(ZIP_DIRECTORY, name, "Function")
    print("Success!")
    # return LAMBDA_CLIENT.create_function(
    #     FunctionName=name,
    #     Runtime="python3.8",
    #     Role="cmgame",
    #     Handler="lambda_handler",
    #     Code={"ZipFile": data},
    #     Layers=[layer_arn],
    # )


# response = client.delete_function(FunctionName="cmgame-test", Qualifier="string")
# pprint(response)
# response = client.create_function(
#     FunctionName=config["name"],
#     Runtime="python3.6",
#     Role="cmgame",
#     Handler="lambda_handler",
#     Code={"ZipFile": code},
#     Layers=[""],
# )
