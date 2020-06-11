from os import path
from typing import Dict, Any, Optional, Callable, List

import boto3  # noqa
from botocore.exceptions import ClientError  # noqa

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


def get_list(
    lambda_function, field: str, key: str, value: str, *args, **kwargs
) -> Dict[str, str]:
    results = lambda_try(lambda_function, *args, **kwargs)
    if results is None:
        print(f"{field} unable to get list.")
        quit()
    if field not in results or not all(
        all(key in layer.keys() for layer in results[field]) for key in (key, value)
    ):
        print(f"Unexpected results: {results}")
        quit()
    ret = results[field]
    if len(ret) == 0:
        print(f"{field} list returned empty.")
    return {entry[key]: entry[value] for entry in ret}


def get_function_layers(function_name: str) -> Dict[str, str]:
    return get_list(
        lambda_function=LAMBDA_CLIENT.get_function_configuration,
        field="Layers",
        key="Arn",
        value="CodeSize",
        FunctionName=function_name,
    )


def get_layers() -> Dict[str, str]:
    return get_list(
        lambda_function=LAMBDA_CLIENT.list_layers,
        field="Layers",
        key="LayerName",
        value="LayerArn",
    )


def get_functions() -> Dict[str, str]:
    return get_list(
        lambda_function=LAMBDA_CLIENT.list_functions,
        field="Functions",
        key="FunctionName",
        value="FunctionArn",
    )


def get_current(deployment_type: str) -> Dict[str, str]:
    if deployment_type == "function":
        return get_functions()
    elif deployment_type == "layer":
        return get_layers()
    else:
        print("Misuse of deployment_utils.get_list().")
        quit()


def publish_layer(layer_name: str, zip_name: str) -> Dict[str, Any]:
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
def update_function(
    function_name: str, zip_name: str, layers: List[str]
) -> Dict[str, Any]:
    data = data_try(zip_name, "Function")
    print("Success!")
    # return LAMBDA_CLIENT.update_function_code(FunctionName=name, ZipFile=data)


def create_function(
    function_name: str, zip_name: str, layers: List[str]
) -> Dict[str, Any]:
    # layers = get_layers()
    # if len(layers) <= 0:
    #     data = data_try(zip_name, "Function")
    #     return {"FunctionName": function_name, "FunctionArn": "string"}

    # function_layers = input_layers_for_function(layers)
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
