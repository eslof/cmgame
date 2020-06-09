from os import path
from typing import Dict, Any

import boto3

from deployment_properties import ZIP_DIRECTORY

LAMBDA_CLIENT = boto3.client("lambda")


def get_layers() -> Dict[str, str]:
    return {
        getattr(layer, "LayerName", ""): getattr(layer, "LayerArn", "")
        for layer in getattr(LAMBDA_CLIENT.list_layers(), "Layers", {})
    }


def get_functions() -> Dict[str, str]:
    return {
        getattr(function, "FunctionName", ""): getattr(function, "FunctionArn", "")
        for function in getattr(LAMBDA_CLIENT.list_functions(), "Functions", {})
    }


def publish_layer(name: str, zip_name: str) -> str:
    if not path.exists(zip_name):
        print(f"Zip file not found: {zip_name} for {name}.")
        raise Exception
    with open(f"{ZIP_DIRECTORY}/{zip_name}", "rb") as rb_f:
        data = rb_f.read()
    if not data:
        print(f"Unable to read zip file: {zip_name} for {name}.")
        raise Exception
    return getattr(
        LAMBDA_CLIENT.publish_layer_version(
            LayerName=name, Content={"ZipFile": data}, CompatibleRuntimes=["python3.8"],
        ),
        "LayerArn",
        "",
    )


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
