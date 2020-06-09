from os import path
from typing import Dict, Any, Optional

import boto3
from botocore.exceptions import ClientError

from deployment_properties import ZIP_DIRECTORY

LAMBDA_CLIENT = boto3.client("lambda")


def lambda_try(lambda_function, *args, **kwargs) -> Optional[Dict[str, Any]]:
    try:
        results = lambda_function(args, kwargs)
    except ClientError as e:
        return None
    except Exception:
        return None
    else:
        return results or {}


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


def publish_layer(name: str, zip_name: str) -> str:
    if not path.exists(zip_name):
        print(f"Layer zip file not found: {zip_name} for {name}.")
        quit()
    with open(f"{ZIP_DIRECTORY}/{zip_name}", "rb") as rb_f:
        data = rb_f.read()
    if not data:
        print(f"Unable to read layer zip file: {zip_name} for {name}.")
        quit()
    results = lambda_try(
        LAMBDA_CLIENT.publish_layer_version,
        LayerName=name,
        Content={"ZipFile": data},
        CompatibleRuntimes=["python3.8"],
    )
    if results is None:
        print(f"Unable to publish layer: {name}.")
        quit()
    if "LayerArn" not in results:
        print(f'Unexpected results: "LayerArn" not in {results}')
        quit()
    return results["LayerArn"]  # type: str


# region Not done
def update_function(name: str) -> Dict[str, Any]:
    return  # TODO: finish
    with open(f"{ZIP_DIRECTORY}/{name}.zip", "rb") as rb_f:
        data = rb_f.read()
    if not data:
        print(f"Unable to read zip file: {name}.zip.")
        raise Exception
    return LAMBDA_CLIENT.update_function_code(FunctionName=name, ZipFile=data)


def create_function(name: str, layer_arn: str) -> Dict[str, Any]:
    return  # TODO: finish
    with open(f"{ZIP_DIRECTORY}/{name}.zip", "rb") as rb_f:
        data = rb_f.read()
    if not data:
        print(f"Unable to read zip file: {name}.zip.")
        raise Exception
    return LAMBDA_CLIENT.create_function(
        FunctionName=name,
        Runtime="python3.8",
        Role="cmgame",
        Handler="lambda_handler",
        Code={"ZipFile": data},
        Layers=[layer_arn],
    )


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
